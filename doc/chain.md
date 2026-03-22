# `Chain` Configuration Syntax

Here is an example configuration for the routes of the login page:

```json
"routes": {
    "/auth/login": [
        ["get", "idents=login.idents@page", "end"],
        ["post", "injest=login.json@page", 
            ["data_eq=password@auth-method", [
                    ["data_eq=on@register", "register", "pw_set", 
                        "session_start", "redir=/auth/dashboard", "end"],
                    ["data_neq=on@register", "pw_auth", 
                        "session_start", "redir=/auth/dashboard", "end"]
                ]
            ],
            ["idents=login.idents@page", "end"]
        ]
    ]
}
```

At a high level this is loading and processing a login page. Becuase this
example uses the Provider service ([polyvinyl/provider/serve.py]), all of the
`tag` values of the identifiers will reference functions defined in
[provider/handlers.py](polyvinyl/provider/handlers.py).

Let's break down what this is doing:

- When the server recieves the page "/auth/login" this configuration entry is used.

```jsonc
"routes": {
    // Serve the following config for a page http://<host>/auth/login
    "/auth/login": [
        // ...
    ]
}
```

- If the method of the requests is GET, it then maps the "path" value from the
  `req` object into the "action" value of the `data` for the request,

```jsonc
"routes": {
    "/auth/login": [
        [   
            // Ensure this is a GET request
            "get",
            // Load and run a file of of identifiers from the page folder 
            "idents=login.idents@page",
            "end"
            // Finish and send request
            "end"
        ],
        // ...
}
```


- The second branch of the sub-chain will be run if any identifier in the first
  branch failed (and raised a DingerKnockout exception). In this case if the
  request was not GET we can expect the second sub-chain to run.

```jsonc
"routes": {
    "/auth/login": [
        ["get", "idents=login.idents@page", "end"],
        // If not GET the next branch will run
        [
            // Ensure the request method is POST
            "post",  
            // Copy values from the form submission, using a definition in the
            // forms json file
            "injest=login.json@page",
            [
                // ...
            ]
    ]
}
```

- Then, once the form data has been recieved, the form has two optional paths:
  register or login.

```jsonc
"routes": {
    "/auth/login": [
        ["get", "map=action/path@req", "content=login-form.format@page", "end"],
        ["post", "map=email,auth-method,password?,fullname?@form", 
            [
                // Proceed with this subchain if data["register"] == "on"
                "data_eq=on@register",
                // Register a new user by running a function 
                "register",
                // Set a password by running a functino 
                "pw_set"
                // Start the session and set a cookie in the headers
                "session_start", 
                // Set the http request redirect properties
                "redir=/auth/dashboard", 
                // Set the request as `done`
                "end"
            ],
            [
                // Proceed with this subchain if data["register"] != "on"
                "data_neq=on@register", 
                // Check that the password is valid 
                "pw_auth"
                // Start the session and set a cookie in the headers
                "session_start", 
                // Set the http request redirect properties
                "redir=/auth/dashboard", 
                // Set the request as `done`
                "end"
        ]
        // ...
    ]
}
```

```jsonc
"routes": {
    "/auth/login": [
        ["get", "map=action/path@req", "content=login-form.format@page", "end"],
        ["post", "map=email,auth-method,password?,fullname?@form", 
            ["data_eq=on@register", "register", "pw_set", 
                "session_start", "redir=/auth/dashboard", "end"],
            ["data_neq=on@register", "pw_auth",
                "session_start", "redir=/auth/dashboard", "end"]

            // This runs if an "end" was not reached above 
            // (meaning something failed and raised a Knockout exception)
            [
                // Load the login page, this time it will have error
                // values to display to the user
                "idents=login.idents@page", 
                // Set the request as `done`
                "end"
            ]
        ]
    ]
}
```

While it is increadibly condensed, it is very easy to converse about the steps
of the system at a high level, without needing to dig through layers of code to
find the order of operations.

See the full configuration example here: [examples/config.json](examples/config.json)

Example handler files can be found [here](polyvinyl/auth/handlers.py) and
[here](polyvinyl/provider/handlers.py). The chain system itself can be found
[here](polyvinyl/utils/handler.py).
