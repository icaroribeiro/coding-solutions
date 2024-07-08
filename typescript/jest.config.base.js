/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  moduleFileExtensions: ["ts", "js"],
  testMatch: ["**/*.test.+(ts|js)"],
  transform: {
    "^.+\\.(ts)$": "ts-jest",
  },
  moduleNameMapper: {
    "^/opt/nodejs/(.*)": "../../../packages/*/src",
  },
};
