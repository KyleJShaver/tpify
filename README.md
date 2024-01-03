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
