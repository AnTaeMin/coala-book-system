#!/usr/bin/env node
// Export the validated manuscript model for independent print production.
const fs = require('node:fs');
const path = require('node:path');
const swc = require('@swc/core');
require.extensions['.ts'] = (module, filename) => {
  const { code } = swc.transformSync(fs.readFileSync(filename, 'utf8'), {
    filename, jsc: { parser: { syntax: 'typescript' }, target: 'es2022' },
    module: { type: 'commonjs' },
  });
  module._compile(code, filename);
};
const { checkBookMarkdown } = require('../src/parser/markdown-book.ts');
const [source, destination] = process.argv.slice(2);
if (!source || !destination) throw new Error('Usage: export-book-spec.cjs source.md destination.json');
const { spec, issues } = checkBookMarkdown(fs.readFileSync(source, 'utf8'));
if (!spec || issues.some(issue => issue.severity === 'error')) throw new Error(JSON.stringify(issues));
fs.mkdirSync(path.dirname(destination), { recursive: true });
fs.writeFileSync(destination, JSON.stringify(spec, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ pages: spec.pages.length, issues, destination }));
