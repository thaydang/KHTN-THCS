import { setTimeout as delay } from "timers/promises";

type TimeoutHandle = ReturnType<typeof setTimeout>;

interface CallGeminiOptions {
    apiKey: string;
    prompt: string;
    model?: string;
    systemPrompt?: string;
    temperature?: number;
    maxOutputTokens?: number;
    timeoutMs?: number;
}

interface GeminiResponsePart {
    text?: string;
}

interface GeminiResponse {
    candidates?: Array<{
        content?: {
            parts?: GeminiResponsePart[];
        };
    }>;
    promptFeedback?: {
        blockReason?: string;
    };
    error?: {
        message?: string;
    };
}

const DEFAULT_MODEL = "gemini-1.5-pro";
const DEFAULT_TEMPERATURE = 0.4;
const MAX_RETRIES = 4;
const BASE_DELAY_MS = 500;
const MAX_DELAY_MS = 4000;
const RETRY_STATUS_CODES = new Set([408, 409, 425, 429, 500, 502, 503, 504]);

function buildRequestBody(options: CallGeminiOptions) {
    const { prompt, systemPrompt, temperature, maxOutputTokens } = options;

    const body: Record<string, unknown> = {
        contents: [
            {
                role: "user",
                parts: [{ text: prompt }],
            },
        ],
    };

    if (systemPrompt) {
        body.systemInstruction = {
            role: "system",
            parts: [{ text: systemPrompt }],
        };
    }

    const generationConfig: Record<string, unknown> = {
        temperature: typeof temperature === "number" ? temperature : DEFAULT_TEMPERATURE,
    };
    if (typeof maxOutputTokens === "number") {
        generationConfig.maxOutputTokens = maxOutputTokens;
    }

    body.generationConfig = generationConfig;

    return body;
}

function shouldRetry(status: number | undefined, error: unknown): boolean {
    if (typeof status === "number") {
        if (RETRY_STATUS_CODES.has(status)) {
            return true;
        }
        if (status >= 500) {
            return true;
        }
        return false;
    }

    if (error instanceof Error) {
        const retryableErrors = ["ETIMEDOUT", "ECONNRESET", "ECONNREFUSED", "ENOTFOUND", "EAI_AGAIN", "EBUSY"];
        // @ts-expect-error Node error objects may include a `code` property.
        const code = error.code as string | undefined;
        if (code && retryableErrors.includes(code)) {
            return true;
        }
        if (error.name === "AbortError") {
            return true;
        }
    }

    return false;
}

function extractText(response: GeminiResponse): string {
    const candidate = response.candidates?.[0];
    if (!candidate?.content?.parts?.length) {
        const blockReason = response.promptFeedback?.blockReason;
        const errorMessage = response.error?.message;
        const reason = blockReason || errorMessage || "unknown reason";
        throw new Error(`Gemini API returned no content (${reason})`);
    }

    const text = candidate.content.parts
        ?.map((part) => part.text ?? "")
        .join("")
        .trim();

    if (!text) {
        throw new Error("Gemini API returned empty content");
    }

    return text;
}

export async function callGemini(options: CallGeminiOptions): Promise<string> {
    const { apiKey, timeoutMs } = options;
    if (!apiKey) {
        throw new Error("Missing Gemini API key");
    }

    const model = options.model ?? DEFAULT_MODEL;
    const body = buildRequestBody(options);
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;

    let attempt = 0;
    let lastError: unknown;

    while (attempt < MAX_RETRIES) {
        const controller = new AbortController();
        const timer: TimeoutHandle | undefined = timeoutMs
            ? (setTimeout(() => controller.abort(), timeoutMs) as TimeoutHandle)
            : undefined;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-goog-api-key": apiKey,
                },
                body: JSON.stringify(body),
                signal: controller.signal,
            });

            if (typeof timer !== "undefined") {
                clearTimeout(timer);
            }

            if (!response.ok) {
                let errorBody: GeminiResponse | undefined;
                try {
                    errorBody = (await response.json()) as GeminiResponse;
                } catch (error) {
                    // Ignore JSON parsing errors for error responses.
                }

                const message = errorBody?.error?.message || `Gemini API request failed with status ${response.status}`;
                if (shouldRetry(response.status, undefined) && attempt < MAX_RETRIES - 1) {
                    attempt += 1;
                    const backoff = Math.min(MAX_DELAY_MS, BASE_DELAY_MS * 2 ** (attempt - 1));
                    await delay(backoff + Math.random() * 250);
                    continue;
                }

                throw new Error(message);
            }

            const data = (await response.json()) as GeminiResponse;
            return extractText(data);
        } catch (error) {
            if (typeof timer !== "undefined") {
                clearTimeout(timer);
            }

            lastError = error;
            const retryable = shouldRetry(undefined, error);
            if (!retryable || attempt >= MAX_RETRIES - 1) {
                if (error instanceof Error) {
                    throw error;
                }
                throw new Error("Unknown error while calling Gemini API");
            }

            attempt += 1;
            const backoff = Math.min(MAX_DELAY_MS, BASE_DELAY_MS * 2 ** (attempt - 1));
            await delay(backoff + Math.random() * 250);
        }
    }

    if (lastError instanceof Error) {
        throw lastError;
    }

    throw new Error("Failed to call Gemini API after multiple retries");
}
