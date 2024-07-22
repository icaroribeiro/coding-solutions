import { sum } from "./../src/index";
import { beforeEach, describe, expect, test, vi } from "vitest";

describe("A", () => {
	beforeEach(() => {
		vi.resetAllMocks();
	});

	test("", () => {
		const result = sum(1, 2);
		expect(result).toEqual(3);
	});
});
