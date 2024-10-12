/** @type {import('prettier').Config} */
module.exports = {
  plugins: ["prettier-plugin-packagejson", "@ianvs/prettier-plugin-sort-imports", "prettier-plugin-organize-imports", "prettier-plugin-tailwindcss"],
  tailwindConfig: "./tailwind.config.cjs",
};
