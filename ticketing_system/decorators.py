from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

# --- tenacity @retry ---
# Rather than writing our own retry logic, we use the battle-tested tenacity library.
# This example shows retry configuration you would apply to an external API call.


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(ConnectionError),
    reraise=True,
)
def call_external_payment_api(customer_name: str, amount: float) -> dict:
    """Example of using tenacity's @retry on an external API call.

    Args:
        customer_name: Customer making the payment.
        amount: Amount to charge.

    Returns:
        Payment API response dict.

    Raises:
        ConnectionError: If the API is unreachable after 3 attempts.
    """
    print(f'[ExternalAPI] Attempting payment for {customer_name}: ${amount:.2f}')
    # In reality this would call an HTTP endpoint.
    # Raising ConnectionError here would trigger automatic retries.
    return {'status': 'ok', 'customer': customer_name, 'amount': amount}


if __name__ == '__main__':
    result = call_external_payment_api('Jane', 9.99)
    print(f'API result: {result}')
