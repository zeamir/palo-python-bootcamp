class TicketingSystemError(Exception):
    """Base for all ticketing system errors."""


class ValidationError(TicketingSystemError, ValueError):
    """Base for data validation failures."""


class BlankMovieNameError(ValidationError):
    """Movie name is blank or whitespace-only."""


class InvalidReleaseYearError(ValidationError):
    """Movie release year is too far in the future."""


class InvalidEmailError(ValidationError):
    """Customer email address is malformed."""


class InvalidPriceError(ValidationError):
    """Ticket or promotion price is not a positive value."""


class InvalidDiscountError(ValidationError):
    """Discount percent is outside the 0-100 range."""


class InvalidTicketCountError(ValidationError):
    """Ticket count (min or max) is not a positive value."""


class InvalidTicketRangeError(ValidationError):
    """max_tickets is less than min_tickets."""


class BookingError(TicketingSystemError, ValueError):
    """Base for booking business-rule violations."""


class MovieNotFoundError(BookingError):
    """Requested movie does not exist in the system."""


class AgeRequirementError(BookingError):
    """Customer does not meet the movie's minimum age requirement."""


class PaymentError(TicketingSystemError, RuntimeError):
    """Base for payment failures."""


class PaymentFailedError(PaymentError):
    """Payment processor declined or failed the transaction."""
