// eslint.config.js

import js from "@eslint/js";
import react from "eslint-plugin-react";
import hooks from "eslint-plugin-react-hooks";
import a11y from "eslint-plugin-jsx-a11y";
import importPlugin from "eslint-plugin-import";

export default [
  js.configs.recommended,
  {
    files: ["**/*.js", "**/*.jsx"],
    ignores: ["dist", "node_modules"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        browser: true,
        node: true,
      },
    },
    plugins: {
      react,
      "react-hooks": hooks,
      "jsx-a11y": a11y,
      import: importPlugin,
    },
    rules: {
      // 🌿 Base
      "no-unused-vars": "warn",
      "no-console": "off",

      // ⚛️ React
      "react/react-in-jsx-scope": "off", // inutile avec React 17+
      "react/prop-types": "off", // désactive PropTypes si tu utilises TypeScript ou non strictement
      "react/jsx-uses-react": "off",

      // 🪝 Hooks
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      // 🔗 Imports
      "import/order": ["warn", { groups: [["builtin", "external", "internal"]] }],

      // ♿ Accessibilité
      "jsx-a11y/alt-text": "warn",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
];
