## How to Use in VSCode

Install the Jupyter extension for VSCode.

```bash
uv venv
source .venv/bin/activate
uv sync --locked
# For the flask part, you can do uv sync --locked --all-extras
```

If you encounter issues selecting the kernel, run the following command: 
```bash
python -m ipykernel install --user --name=my-uv-env --display-name "Python (uv-env)"
```
Then press `Ctrl+Shift+P` (or `Cmd+Shift+P`), type **`Developer: Reload Window`**, and press Enter.  
Now, click the kernel selection button in the top right of your notebook again, and you will see the new kernel sitting there waiting for you in "Python environments".

To highlight the CSV content, you can install the "Rainbow CSV" extension.