# SchedJulia Wrapper

Wrapper written in Python around [SchedJulia](https://gitlab.com/leglesslamb/schedjulia) to schedule interviews.

## Overview

This wrapper reads interview groups and availabilities from a Google Sheet, generates a schedule with [SchedJulia](https://gitlab.com/leglesslamb/schedjulia), and pushes ths schedule to another Google Sheet. It converts to and from SchedJulia-format when using SchedJulia.

### Prerequisites

- [Julia](https://julialang.org/).
- [Python](https://www.python.org/).
  - [pip](https://pypi.org/project/pip/).

### Dependencies

- [Google Sheets API for Python](https://developers.google.com/sheets/api/quickstart/python).
  - [google-api-python-client](https://pypi.org/project/google-api-python-client/).
  - [google-auth-httplib2](https://pypi.org/project/google-auth-httplib2/).
  - [google-google-auth-oauthlib](https://pypi.org/project/google-google-auth-oauthlib/).
- [SchedJulia](https://gitlab.com/leglesslamb/schedjulia).

### Setup

- Clone the repository and initialize the SchedJulia submodule.

  ```sh
  git clone https://gitlab.com/utmist/schedjulia-wrapper.git
  git submodule update --init --recursive
  ```

- Install dependencies.

  ```sh
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
  ```

## Development

- This project is maintained by the [Infrastructure Department at UTMIST](https://utmist.gitlab.io/team/infrastructure).
  - [Robbert Liu](https://github.com/triglemon), Infrastructure Developer.
  - [Robert (Rupert) Wu](https://leglesslamb.gitlab.io), VP Infrastructure.
- If you're a member of UTMIST and would like to contribute or learn development through this project, you can join our [Discord](https://discord.gg/88mSPw8)) and let us know in _#infrastructure_.
