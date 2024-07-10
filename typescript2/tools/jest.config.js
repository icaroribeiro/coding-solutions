/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  rootDir: "../src",
  testMatch: ["**/*.test.ts"],
  moduleNameMapper: {
    "^/opt/nodejs/(.*)": "./src/shared/(.*)",
  },
  transform: {
    "^.+\\.tsx?$": "ts-jest",
  },
};
