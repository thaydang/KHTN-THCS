// @ts-check
/**
 * Công cụ Google Apps Script để xuất bản release GitHub.
 * Giữ nguyên API công khai như bản gốc nhưng bổ sung kiểm tra lỗi rõ ràng hơn
 * và loại bỏ đoạn mã trùng lặp.
 */

/** @typedef {GoogleAppsScript.Properties.Properties} ScriptProperties */
/** @typedef {GoogleAppsScript.Base.Blob} Blob */

/**
 * @typedef GitHubConfig
 * @property {string} owner
 * @property {string} repo
 * @property {string} token
 * @property {string} api
 */

/**
 * @returns {GitHubConfig}
 */
function loadGitHubConfig() {
  var props = PropertiesService.getScriptProperties();
  var owner = props.getProperty('GITHUB_OWNER');
  var repo = props.getProperty('GITHUB_REPO');
  var token = props.getProperty('GITHUB_TOKEN');

  if (!owner) throw new Error('Thiếu Script property GITHUB_OWNER');
  if (!repo) throw new Error('Thiếu Script property GITHUB_REPO');
  if (!token) throw new Error('Thiếu Script property GITHUB_TOKEN');

  return {
    owner: owner,
    repo: repo,
    token: token,
    api: 'https://api.github.com',
  };
}

/** @type {GitHubConfig} */
var GH = loadGitHubConfig();

/**
 * @param {string} path
 * @param {{ method?: GoogleAppsScript.URL_Fetch.HttpMethod, payload?: string | GoogleAppsScript.Base.BlobSource, contentType?: string }} [opts]
 */
function ghFetch(path, opts) {
  if (!GH.token) throw new Error('Thiếu Script property GITHUB_TOKEN');

  var url = GH.api + path;
  var headers = {
    Authorization: 'token ' + GH.token,
    Accept: 'application/vnd.github+json',
    'User-Agent': 'apps-script',
  };

  var response = UrlFetchApp.fetch(url, {
    method: (opts && opts.method) || 'get',
    muteHttpExceptions: true,
    headers: headers,
    payload: opts && opts.payload,
    contentType: opts && opts.contentType,
  });

  var code = response.getResponseCode();
  var body = response.getContentText();

  if (code >= 400) {
    throw new Error('GitHub ' + code + ': ' + body);
  }

  return body ? JSON.parse(body) : {};
}

/**
 * @param {string} tag
 * @param {string} title
 * @param {string} [body]
 * @param {boolean} [draft]
 * @param {boolean} [prerelease]
 * @param {string} [target]
 */
function createRelease(tag, title, body, draft, prerelease, target) {
  var payload = JSON.stringify({
    tag_name: tag,
    target_commitish: target || 'main',
    name: title || tag,
    body: body || '',
    draft: Boolean(draft),
    prerelease: Boolean(prerelease),
    generate_release_notes: false,
  });

  return ghFetch('/repos/' + GH.owner + '/' + GH.repo + '/releases', {
    method: 'post',
    payload: payload,
    contentType: 'application/json',
  });
}

/**
 * @param {string} tag
 * @returns {any | null}
 */
function getReleaseByTag(tag) {
  try {
    return ghFetch('/repos/' + GH.owner + '/' + GH.repo + '/releases/tags/' + encodeURIComponent(tag));
  } catch (error) {
    if (String(error).indexOf('404') !== -1) return null;
    throw error;
  }
}

/**
 * @param {string} uploadUrl
 * @param {string} fileId
 */
function uploadAsset(uploadUrl, fileId) {
  var file = DriveApp.getFileById(fileId);
  var name = file.getName();
  var blob = file.getBlob();

  var url = uploadUrl.replace('{?name,label}', '?name=' + encodeURIComponent(name));
  var headers = {
    Authorization: 'token ' + GH.token,
    'Content-Type': blob.getContentType(),
    Accept: 'application/vnd.github+json',
    'User-Agent': 'apps-script',
  };

  var res = UrlFetchApp.fetch(url, {
    method: 'post',
    headers: headers,
    muteHttpExceptions: true,
    payload: blob.getBytes(),
  });

  var code = res.getResponseCode();
  if (code >= 400) {
    throw new Error('Upload asset fail ' + code + ': ' + res.getContentText());
  }

  var text = res.getContentText();
  return text ? JSON.parse(text) : {};
}

function publishReleaseFromDrive() {
  var TAG = 'v2025.11.05';
  var TITLE = 'KHTN-THCS – phát hành giáo án & đề mẫu';
  var DESC = [
    '### Nội dung',
    '- Cập nhật giáo án khối 8 chương 1',
    "- Bổ sung đề kiểm tra 15′ chương 2",
    '- Sửa lỗi export DOCX',
    '',
    '### Ghi chú',
    'Theo chuẩn CV5512 & 7991.',
  ].join('\n');

  /** @type {string[]} */
  var FILE_IDS = [];

  var existed = getReleaseByTag(TAG);
  if (existed) {
    throw new Error('Tag ' + TAG + ' đã tồn tại. Hãy tăng version (vd: v2025.11.05-1).');
  }

  var rel = createRelease(TAG, TITLE, DESC, false, false, 'main');

  for (var i = 0; i < FILE_IDS.length; i += 1) {
    uploadAsset(rel.upload_url, FILE_IDS[i]);
  }

  Logger.log('OK: ' + rel.html_url);
  return rel.html_url;
}

/**
 * @param {string} [titlePrefix]
 * @param {string} [body]
 */
function createPatchReleaseAuto(titlePrefix, body) {
  var rels = ghFetch('/repos/' + GH.owner + '/' + GH.repo + '/releases?per_page=1');
  var next = 'v1.0.0';

  if (rels && rels.length) {
    var latest = String(rels[0].tag_name || '');
    var match = latest.match(/^v(\d+)\.(\d+)\.(\d+)$/);
    if (match) {
      var major = Number(match[1]);
      var minor = Number(match[2]);
      var patch = Number(match[3]);
      next = 'v' + major + '.' + minor + '.' + (patch + 1);
    }
  }

  var rel = createRelease(next, (titlePrefix || 'Auto Release') + ' ' + next, body || '');
  Logger.log(rel.html_url);
  return rel.html_url;
}

function testGitHubToken() {
  var token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('Thiếu Script property GITHUB_TOKEN');

  var res = UrlFetchApp.fetch('https://api.github.com/user', {
    headers: {
      Authorization: 'token ' + token,
      'User-Agent': 'apps-script',
    },
  });

  Logger.log(res.getContentText());
}
