module.exports = {
  moduleFileExtensions: ["ts", "js"],
  testMatch: ["**/*.test.+(ts|js)"],
  transform: {
    "^.+\\.(ts)$": "ts-jest",
  },
  moduleNameMapper: {
    "@package/(.*)": "<rootDir>/src/$1",
  },
  globals: {
    "ts-jest": {
      tsConfigFile: "tsconfig.json",
    },
  },
};
