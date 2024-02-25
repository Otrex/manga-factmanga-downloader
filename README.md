## On Start

Run the following below to start.
First generate a venv configuration.

Run the command:

```bash
pip3 install venv
```

Then run

```bash
python -m venv .
```

Then switch to the venv source by running the command

```bash
source bin/activate
```

Then run `pip install -r requirements.txt` to install the requirements

```bash
uvicorn src.server:app --reload --port 8080
```

To get the folder, use the URL

```bash
http://127.0.0.1:8080/read/avalon-of-disaster
```
