const mockResponse = {
  success: true,
  resolution: {
    type: "replacement",
    message: "Your replacement request has been successfully processed.",
    orderId: "ORD-10245",
    status: "confirmed",
  },
};

export async function resolveCustomerIssue(issue) {
  // Simulate API processing delay
  await new Promise((resolve) => setTimeout(resolve, 2000));

  if (!issue || !issue.trim()) {
    throw new Error("Please describe your issue.");
  }

  return mockResponse;
}