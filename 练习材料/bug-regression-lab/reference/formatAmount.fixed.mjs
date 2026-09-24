export function formatAmount(value) {
  if (value === undefined) {
    return "--";
  }

  return `¥${Number(value).toFixed(2)}`;
}
