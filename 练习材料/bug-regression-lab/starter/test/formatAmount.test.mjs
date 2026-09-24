import test from "node:test";
import assert from "node:assert/strict";
import { formatAmount } from "../src/formatAmount.mjs";

test("formats a decimal amount with two places", () => {
  assert.equal(formatAmount(12.5), "¥12.50");
});

test("keeps zero as a valid amount", () => {
  assert.equal(formatAmount(0), "¥0.00");
});
