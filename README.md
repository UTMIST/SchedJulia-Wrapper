# UTMIST Scheduler

Wrapper written in Python around [SchedJulia](https://gitlab.com/leglesslamb/schedjulia) to schedule interviews.

## Overview

This wrapper reads interview groups and availabilities from a Google Sheet, generates a schedule with [SchedJulia](https://gitlab.com/leglesslamb/schedjulia), and pushes ths schedule to another Google Sheet. It converts to and from SchedJulia-format when using SchedJulia.

### Prerequisites

- [Julia](https://julialang.org/)
- [Python](https://www.python.org/)
  - [pip](https://pypi.org/project/pip/)

### Dependencies

- [Google Sheets API for Python](https://developers.google.com/sheets/api/quickstart/python)
  - [google-api-python-client](https://pypi.org/project/google-api-python-client/)
  - [google-auth-httplib2](https://pypi.org/project/google-auth-httplib2/)
  - [google-google-auth-oauthlib](https://pypi.org/project/google-google-auth-oauthlib/)
- [os.path](https://docs.python.org/3/library/os.path.html)
- [pickle](https://docs.python.org/3/library/pickle.html)
- [SchedJulia](https://gitlab.com/leglesslamb/schedjulia)

### Setup

- Clone the repository and initialize the SchedJulia submodule.

  ```sh
  git clone https://gitlab.com/utmist/schedjulia-wrapper.git
  git submodule update --init --recursive
  ```

- Install dependencies.

  ```sh
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv
  ```

- Load environment variables in `.env`. A blank copy `copy.env` lists the required variables with sample variables from the 2020 summer period. The formats will be documented in the future.

- Place `credentials.json` from the [Google Sheets API](https://developers.google.com/sheets/api/quickstart) in the root directory.

## Usage

Run `script.sh`.

### Troubleshooting

- One bug encountered was expiration of Google Sheets API authentication. Problem might be solved by refreshing `credentials.json` or deleting `token.pickle`.

## Development

- This project is maintained by the [Infrastructure Department at UTMIST](https://utmist.gitlab.io/team/infrastructure).
  - [Robert (Rupert) Wu](https://leglesslamb.gitlab.io), VP Infrastructure.
  - [Robbert Liu](https://github.com/triglemon), Infrastructure Developer.
- If you're a member of UTMIST and would like to contribute or learn development through this project, you can join our [Discord](https://discord.gg/88mSPw8)) and let us know in _#infrastructure_.
