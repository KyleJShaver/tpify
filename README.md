# tpify
_Pronounced like "typify"_

Make Python calls respond like HTTP requests.

## What this does
**tpify** allows you to request functions return HTTP-like response objects, along with HTTP status codes.

## Why?
### No more `try`/`except`
Since all tpified functions return an object, there is no need to wrap functions in a `try` block. This leads to safer, more predictable execution paths. Exceptions are still returned in the `Response` when raised, and the ability to customize which HTTP status code is returned means the code can easily communicate whether the exception came from internal logic or input data.

### Better statuses
Since `Response` objects contain HTTP status codes, you can provide better context about successes and failures. For example:
* Functions that return `True` can return context about whether a new resource was created using `201`.
* Functions that return `None` can return information about whether `None` means a successful or failed execution.
* Failures can be returned that indicate if the error is an error with the provided data (`4XX` responses), or with the processing of the data iteself (`5XX` responses).
