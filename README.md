# tpify
_Pronounced like "[typify](https://www.dictionary.com/browse/typify)"_

Return, don't raise.

## What this does
**tpify** allows you to configure functions to return contextual statuses, and to return errors rather than raise them.

## Why?
Python programs often have inconsistent conventions when it comes to returning data. They also have a problem of not making it clear when exceptions can be raised. This is an attempt to see if there is enough benefit to violate Pythonic conventions to get some additional reliability and improved (albeit verbose, [Go-like](https://go.dev/blog/error-handling-and-go)) error handling.

## Benefits
### No more `try`/`except`
All tpified functions return an object, removing the need to wrap functions in a `try` block. This leads to safer, more predictable execution paths. Exceptions are still returned when raised, and the ability to customize which status code is returned means the type and source of error can be more easily communicated.

### Better context
`TPResponse` objects contain status codes, enabling richer context about successes and failures. For example:
* Functions that return `True` can return context about whether a new resource was created using `tp.Created` status, or updated using the `tp.Updated` status.
* Functions that return `None` can return information about whether `None` means a successful or failed execution.
* Failures can be returned that indicate if the error is an error with the input data (`tp.InputError` responses), or with the processing of the data iteself (`tp.ProcessingError` responses).
If you can't find a code that works for you, there is always the option to create your own.

## Dos and Don'ts
**DO: Check your `TPResponse` status codes**. While you _can_ just take the `content` of a `TPResponse` if you only want the safety of avoiding unintended `raise` statements, it is encouraged to have some paradigm to process `status_code` values.

**DO: append `_tp` at the end of tpified function names**. This communicates that this function returns a `TPResponse` object, since the function itself may show it returns a different type.
  ```python
  from tpify import tpify

  @tpify()
  def fibonacci_tp(n: int) -> int:
    # TODO: Implement fibonacci recursively
  ```
**DO: use `@tpify()` after non-return type-modifying decorators**. If you have multiple decorators on a tpified function, have `tpify()` be after those that don't modify return types, so that the return types are accounted for in any other decorator logic.
  ```python
  from functools import cache
  from tpify import tpify

  @cache
  @tpify()
  def fibonacci_tp(n: int):
    # TODO: Implement fibonacci recursively
  ```

