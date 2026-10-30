const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = JSON.parse(fs.readFileSync(path.join(__dirname, 'scripts_for_validation.json'), 'utf8'));
let errors = [];
for (const entry of source) {
  try { new vm.Script(entry.source, {filename: entry.file}); }
  catch (error) { errors.push({file:entry.file,error:String(error)}); }
}
const report = {scripts_checked:source.length,errors,status:errors.length?'failed':'passed'};
const parent = path.resolve(__dirname,'..');
const root = process.env.HTML_WISHLIST_OUTPUT || (fs.existsSync(path.join(parent,'original_wishlist.txt'))?parent:path.join(parent,'html-wishlist-1500'));
fs.writeFileSync(path.join(root,'qa_javascript.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
process.exitCode = errors.length?1:0;
