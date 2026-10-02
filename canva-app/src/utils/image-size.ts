/**
 * 이미지 파일의 픽셀 크기를 헤더만 읽어 알아낸다.
 *
 * 브라우저 밖(검증 명령)에서는 이미지를 디코딩할 수 없으므로 파일 앞부분의
 * 크기 정보만 읽는다. PNG, JPEG, GIF, WebP를 지원한다. 그 밖의 형식이나 깨진
 * 파일은 undefined다.
 */
export type ImageSize = { width: number; height: number };

export function imageSizeOf(bytes: Uint8Array): ImageSize | undefined {
  return pngSize(bytes) ?? jpegSize(bytes) ?? gifSize(bytes) ?? webpSize(bytes);
}

const be32 = (bytes: Uint8Array, at: number) =>
  ((bytes[at] ?? 0) << 24) |
  ((bytes[at + 1] ?? 0) << 16) |
  ((bytes[at + 2] ?? 0) << 8) |
  (bytes[at + 3] ?? 0);
const be16 = (bytes: Uint8Array, at: number) =>
  ((bytes[at] ?? 0) << 8) | (bytes[at + 1] ?? 0);
const le16 = (bytes: Uint8Array, at: number) =>
  (bytes[at] ?? 0) | ((bytes[at + 1] ?? 0) << 8);
const le24 = (bytes: Uint8Array, at: number) =>
  le16(bytes, at) | ((bytes[at + 2] ?? 0) << 16);
const ascii = (bytes: Uint8Array, at: number, length: number) =>
  String.fromCharCode(...bytes.slice(at, at + length));

function pngSize(bytes: Uint8Array): ImageSize | undefined {
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (bytes.length < 24 || !signature.every((b, i) => bytes[i] === b)) {
    return undefined;
  }
  if (ascii(bytes, 12, 4) !== "IHDR") {
    return undefined;
  }
  return { width: be32(bytes, 16), height: be32(bytes, 20) };
}

function jpegSize(bytes: Uint8Array): ImageSize | undefined {
  if (bytes[0] !== 0xff || bytes[1] !== 0xd8) {
    return undefined;
  }
  let at = 2;
  while (at + 9 < bytes.length) {
    if (bytes[at] !== 0xff) {
      at += 1;
      continue;
    }
    const marker = bytes[at + 1] ?? 0;
    if (marker === 0xff) {
      at += 1;
      continue;
    }
    // SOF0~SOF15 (DHT 0xc4, JPG 0xc8, DAC 0xcc 제외)에 크기가 있다.
    const isStartOfFrame =
      marker >= 0xc0 &&
      marker <= 0xcf &&
      marker !== 0xc4 &&
      marker !== 0xc8 &&
      marker !== 0xcc;
    if (isStartOfFrame) {
      return { height: be16(bytes, at + 5), width: be16(bytes, at + 7) };
    }
    if (marker === 0xd9 || marker === 0xda) {
      return undefined;
    }
    at += 2 + be16(bytes, at + 2);
  }
  return undefined;
}

function gifSize(bytes: Uint8Array): ImageSize | undefined {
  if (bytes.length < 10 || ascii(bytes, 0, 3) !== "GIF") {
    return undefined;
  }
  return { width: le16(bytes, 6), height: le16(bytes, 8) };
}

function webpSize(bytes: Uint8Array): ImageSize | undefined {
  if (
    bytes.length < 30 ||
    ascii(bytes, 0, 4) !== "RIFF" ||
    ascii(bytes, 8, 4) !== "WEBP"
  ) {
    return undefined;
  }
  const chunk = ascii(bytes, 12, 4);
  if (chunk === "VP8 ") {
    return {
      width: le16(bytes, 26) & 0x3fff,
      height: le16(bytes, 28) & 0x3fff,
    };
  }
  if (chunk === "VP8L") {
    // VP8L: 서명 0x2f 다음 4바이트에 (폭-1) 14비트, (높이-1) 14비트가 이어진다.
    const b0 = bytes[21] ?? 0;
    const b1 = bytes[22] ?? 0;
    const b2 = bytes[23] ?? 0;
    const b3 = bytes[24] ?? 0;
    return {
      width: 1 + (((b1 & 0x3f) << 8) | b0),
      height: 1 + (((b3 & 0x0f) << 10) | (b2 << 2) | ((b1 & 0xc0) >> 6)),
    };
  }
  if (chunk === "VP8X") {
    return { width: 1 + le24(bytes, 24), height: 1 + le24(bytes, 27) };
  }
  return undefined;
}
