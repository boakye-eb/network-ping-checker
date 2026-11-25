# Network Ping Checker

A small Python script that checks whether a connection problem is with the computer, the router, the internet provider, or DNS. It automates the ping steps from my [IT Support Troubleshooting Guide](https://github.com/boakye-eb/it-support-troubleshooting-guide).

## What it does

It pings three targets in order and prints a plain-English diagnosis:

| Check | Target | What a failure means |
|-------|--------|----------------------|
| Router | your router's IP (e.g. `192.168.1.1`) | The problem is between this computer and the router |
| Public IP | `8.8.8.8` | The router works, but the internet is unreachable (often the provider) |
| Website name | `google.com` | The internet works by IP, so the problem is DNS |

## Requirements

- Python 3.8 or newer
- No extra packages (standard library only)
- Windows, macOS or Linux

## How to run

```
python ping_checker.py
```

It asks for your router's IP address. You can also pass it directly and save the results to a CSV file:

```
python ping_checker.py --router 192.168.1.1 --log results.csv
```

To find your router's IP on Windows, run `ipconfig` and look for **Default Gateway**.

## Example output

> Replace this block with your own real output after running the script.

```
Running checks...

Router          192.168.1.1        UP    3 ms
Public IP       8.8.8.8            UP    164 ms
Website (DNS)   google.com         UP    171 ms

Diagnosis: All three checks passed. The connection looks healthy.
```

## How it works

1. `ping()` runs the system `ping` command 4 times (`-n` on Windows, `-c` on macOS/Linux) and averages the reply times.
2. `diagnose()` combines the three results using the same logic as the guide: router first, then the internet, then DNS.
3. With `--log`, each run is appended to a CSV file so you can compare results over time.

## What I learned

- How to run a system command from Python with `subprocess` and read its output.
- How to pull values out of text with a regular expression.
- How to handle differences between Windows and Linux/macOS in one script.
- That the same ping order I use by hand can be turned into a small tool.

## Ideas for next steps

- Check several websites instead of one
- Run the checks repeatedly and alert when a target goes down
- Add a timestamped log chart
