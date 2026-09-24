import { formatAmount } from "./src/formatAmount.mjs";

const orders = [
  { id: "A-100", amount: 12.5 },
  { id: "A-101" },
];

for (const order of orders) {
  console.log(`${order.id}: ${formatAmount(order.amount)}`);
}
