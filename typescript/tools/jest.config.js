/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  moduleFileExtensions: ["ts", "js"],
  testMatch: ["**/*.test.+(ts|js)"],
  transform: {
    "^.+\\.(ts)$": "ts-jest",
  },
  moduleNameMapper: {
    "@packages/(.*)": "<rootDir>/src/$1",
  },
  globals: {
    "ts-jest": {
      tsConfigFile: "tsconfig.json",
    },
  },
};
