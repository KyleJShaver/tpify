# tpify
_Pronounced like "[typify](https://www.dictionary.com/browse/typify)"_

Make Python calls respond like HTTP requests.

## What this does
**tpify** allows you to request functions return HTTP-like response objects, along with [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

## Why?
HTTP has been around for a long time, and is a well-established standard. Python programs often have inconsistent conventions when it comes to returning data. This is an attempt to see if there is enough benefit to violate Pythonic conventions to get some additional reliability and improved (albeit verbose, [Go-like](https://go.dev/blog/error-handling-and-go)) error handling.

## Benefits
### No more `try`/`except`
All tpified functions return an object, removing the need to wrap functions in a `try` block. This leads to safer, more predictable execution paths. Exceptions are still returned in the `Response.content` when raised, and the ability to customize which HTTP status code is returned means the type and source of error can be more easily communicated.

### Better statuses
`Response` objects contain HTTP status codes, enabling richer context about successes and failures. For example:
* Functions that return `True` can return context about whether a new resource was created using `201`.
* Functions that return `None` can return information about whether `None` means a successful or failed execution.
* Failures can be returned that indicate if the error is an error with the provided data (`4XX` responses), or with the processing of the data iteself (`5XX` responses).
If you can't find an HTTP status code that applies to your use case...are you sure?

## Examples
### JSON parsing
Say we're taking input that we're attempting to parse as JSON. Typically, Python code would look like this:
```python
import json

def load_data():
    data = json.loads('{"a": 1}')
    return data

if __name__ == "__main__":
    data = load_data()
    print(data)
```
> {'a': 1}

Normally this works fine. But let's say there's an issue with the data:
```python
import json

def load_data():
    data = json.loads('{a: 1}')
    return data

if __name__ == "__main__":
    data = load_data()
    print(data)
```
> json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

While [the documentaion for `json.loads()`](https://docs.python.org/3.11/library/json.html#json.loads) does show that a `JSONDecodeError` can be thrown, it's rarely an exception that is handled in practice. Calling `json.loads()`, either as a tpified function itself, or from within a tpified function, will ensure that your code can continue to execute. You can even return a status code that corresponds with whether the data you encountered an error with came from the server side or the client side. Let's see what happens when we call a successful JSON load:

```python
import json
from tpify import tpify

@tpify
def load_data():
    data = json.loads('{"a": 1}')
    return data

if __name__ == "__main__":
    resp = load_data()
    print(resp)
    print(resp.content)
```
><Response [200]><br>
{'a': 1}

In this case, note that tpifying `load_data()` causes it to return a `Response` object. In this case, it has a status code of 200, and a content of the same data returned in the original version.

The cool part comes when there is an issue with the JSON load:
```python
import json
from tpify import tpify

@tpify
def load_data():
    data = json.loads('{a: 1}')
    return data

if __name__ == "__main__":
    resp = load_data()
    print(resp)
    print(resp.content)
```
> <Response [500]><br>
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

Note that with no change to the code, the JSON load error does not cause a crash, and the error can ba handled immediately after it is encountered.
