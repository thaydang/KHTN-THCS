// @ts-check
/**
 * Công cụ Google Apps Script để xuất bản release GitHub.
 * Phiên bản: Refined & Optimized
 */

/** @typedef {GoogleAppsScript.Properties.Properties} ScriptProperties */

/**
 * @typedef GitHubConfig
 * @property {string} owner
 * @property {string} repo
 * @property {string} token
 * @property {string} api
 */

/**
 * Lấy cấu hình GitHub. Sử dụng cơ chế Lazy Loading để tránh lỗi Global.
 * @returns {GitHubConfig}
 */
function getGitHubConfig() {
  const props = PropertiesService.getScriptProperties();
  const owner = props.getProperty('GITHUB_OWNER');
  const repo = props.getProperty('GITHUB_REPO');
  const token = props.getProperty('GITHUB_TOKEN');

  if (!owner || !repo || !token) {
    throw new Error('Thiếu cấu hình: Vui lòng thiết lập GITHUB_OWNER, GITHUB_REPO, và GITHUB_TOKEN trong Script Properties.');
  }

  return {
    owner: owner,
    repo: repo,
    token: token,
    api: 'https://api.github.com',
  };
}

/**
 * Hàm Wrapper cho UrlFetchApp
 * @param {string} path
 * @param {{ method?: GoogleAppsScript.URL_Fetch.HttpMethod, payload?: string | GoogleAppsScript.Base.BlobSource, contentType?: string, rawBlob?: boolean }} [opts]
 */
function ghFetch(path, opts) {
  const cfg = getGitHubConfig(); // Gọi config bên trong hàm
  const url = path.startsWith('http') ? path : cfg.api + path;

  const headers = {
    'Authorization': 'Bearer ' + cfg.token,
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28', // Cố định version API để ổn định
    'User-Agent': 'google-apps-script'
  };

  // Nếu upload file blob, Content-Type sẽ được tự động xử lý bởi UrlFetchApp
  if (opts && opts.contentType) {
    headers['Content-Type'] = opts.contentType;
  }

  const response = UrlFetchApp.fetch(url, {
    method: (opts && opts.method) || 'get',
    muteHttpExceptions: true,
    headers: headers,
    payload: opts && opts.payload
  });

  const code = response.getResponseCode();
  const body = response.getContentText();

  if (code >= 400) {
    throw new Error(`GitHub Error (${code}): ${body}`);
  }

  return body ? JSON.parse(body) : {};
}

/**
 * Tạo Release mới
 * @param {string} tag
 * @param {string} title
 * @param {string} [body]
 * @param {boolean} [draft]
 * @param {boolean} [prerelease]
 * @param {string} [target]
 */
function createRelease(tag, title, body, draft, prerelease, target) {
  const cfg = getGitHubConfig();
  const payload = JSON.stringify({
    tag_name: tag,
    target_commitish: target || 'main',
    name: title || tag,
    body: body || '',
    draft: Boolean(draft),
    prerelease: Boolean(prerelease),
    generate_release_notes: false,
  });

  return ghFetch(`/repos/${cfg.owner}/${cfg.repo}/releases`, {
    method: 'post',
    payload: payload,
    contentType: 'application/json',
  });
}

/**
 * Lấy thông tin Release theo Tag
 * @param {string} tag
 * @returns {any | null}
 */
function getReleaseByTag(tag) {
  const cfg = getGitHubConfig();
  try {
    return ghFetch(`/repos/${cfg.owner}/${cfg.repo}/releases/tags/${encodeURIComponent(tag)}`);
  } catch (error) {
    if (String(error).includes('404')) return null;
    throw error;
  }
}

/**
 * Upload file lên Release Asset
 * @param {string} uploadUrlTemplate - URL trả về từ việc tạo release
 * @param {string} fileId - ID file Google Drive
 */
function uploadAsset(uploadUrlTemplate, fileId) {
  const file = DriveApp.getFileById(fileId);
  const name = file.getName();
  const blob = file.getBlob();

  // GitHub trả về upload_url dạng template: .../assets{?name,label}
  // Cần cắt bỏ phần template phía sau
  const cleanUrl = uploadUrlTemplate.split('{')[0]; 
  const url = `${cleanUrl}?name=${encodeURIComponent(name)}`;

  // Gọi trực tiếp UrlFetchApp tại đây để kiểm soát header Content-Type đặc biệt cho binary
  const cfg = getGitHubConfig();
  const headers = {
    'Authorization': 'Bearer ' + cfg.token,
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'google-apps-script',
    'Content-Type': blob.getContentType() // Quan trọng: Loại nội dung của file
  };

  // LƯU Ý: Truyền trực tiếp đối tượng `blob`, KHÔNG dùng `.getBytes()` để tiết kiệm bộ nhớ
  const res = UrlFetchApp.fetch(url, {
    method: 'post',
    headers: headers,
    payload: blob, 
    muteHttpExceptions: true
  });

  const code = res.getResponseCode();
  if (code >= 400) {
    throw new Error(`Upload asset fail (${code}): ${res.getContentText()}`);
  }

  return JSON.parse(res.getContentText());
}

// --- CÁC HÀM THỰC THI (MAIN FUNCTIONS) ---

function publishReleaseFromDrive() {
  const TAG = 'v2025.11.05'; // Cập nhật tag mới
  const TITLE = 'KHTN-THCS – phát hành giáo án & đề mẫu';
  const DESC = `### Nội dung
- Cập nhật giáo án khối 8 chương 1
- Bổ sung đề kiểm tra 15′ chương 2
- Sửa lỗi export DOCX

### Ghi chú
Theo chuẩn CV5512 & 7991.`;

  // Điền ID file thực tế vào đây
  const FILE_IDS = []; 
  // Ví dụ: const FILE_IDS = ['1xYz...ID_FILE_1...', '1xYz...ID_FILE_2...'];

  const existed = getReleaseByTag(TAG);
  if (existed) {
    throw new Error(`Tag ${TAG} đã tồn tại. Vui lòng cập nhật phiên bản.`);
  }

  Logger.log(`Đang tạo release ${TAG}...`);
  const rel = createRelease(TAG, TITLE, DESC, false, false, 'main');
  
  Logger.log(`Tạo thành công: ${rel.html_url}. Đang upload assets...`);

  for (const fileId of FILE_IDS) {
    try {
      uploadAsset(rel.upload_url, fileId);
      Logger.log(`- Đã upload file ID: ${fileId}`);
    } catch (e) {
      Logger.log(`- Lỗi upload file ID ${fileId}: ${e.message}`);
    }
  }

  Logger.log('Hoàn tất quá trình phát hành.');
  return rel.html_url;
}

/**
 * Tự động tăng phiên bản Patch (x.x.X+1)
 */
function createPatchReleaseAuto(titlePrefix, body) {
  const cfg = getGitHubConfig();
  // Lấy release mới nhất
  const rels = ghFetch(`/repos/${cfg.owner}/${cfg.repo}/releases?per_page=1`);
  let next = 'v1.0.0';

  if (rels && rels.length > 0) {
    const latest = String(rels[0].tag_name || '');
    const match = latest.match(/^v(\d+)\.(\d+)\.(\d+)$/);
    if (match) {
      const major = Number(match[1]);
      const minor = Number(match[2]);
      const patch = Number(match[3]);
      next = `v${major}.${minor}.${patch + 1}`;
    }
  }

  const title = `${titlePrefix || 'Auto Release'} ${next}`;
  const rel = createRelease(next, title, body || 'Tự động phát hành bởi Apps Script');
  
  Logger.log(`Đã tạo Patch Release mới: ${rel.html_url}`);
  return rel.html_url;
}

