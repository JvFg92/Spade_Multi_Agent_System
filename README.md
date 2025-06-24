
## Setting up your environment

### 0. Pre steps:
**On Linux 🐧:**
```bash
sudo apt update
sudo apt install python3-venv python3-full
```

**On Windows 🪟:**
⚠️ *On PowerShell:* ⚠️
```bash
python --version
pip --version
```
*If these commands fail, you may need to reinstall Python, ensuring you check the "Add Python to PATH" option.*

### 1. Virtual enviroment creation Linux/Windows:
```bash
# Create and enter a directory for your project
mkdir my_spade_project
cd my_spade_project

# Create the virtual environment named 'venv'
python3 -m venv venv
```

###  2. Activate the Virtual Environment:
**On Linux 🐧:**
```bash
source venv/bin/activate
```

**On Windows 🪟:**
```bash
.\venv\Scripts\activate
```
*You will know it's active because (venv) will appear at the beginning of your terminal prompt.*

### 3. Install Spade:
```bash
pip install spade
```

### 4. Clone the Repository:
⚠️ **Make sure that you still in the correct directory** ⚠️
```bash
git clone https://github.com/JvFg92/Spade_Multi_Agent_System
```

### 5. Running the scripts: ▶️
**Generator:**
```bash
cd Spade_Multi_Agent_System
python Gerador.py
```

**Solver:**

⚠️ **Open other Terminal** ⚠️

**On Linux 🐧:**
```bash
cd my_spade_project/Spade_Multi_Agent_System
```

```bash
source venv/bin/activate
```

```bash
python3 Resolvedor.py
```

**On Windows 🪟:**
```bash
cd my_spade_project/Spade_Multi_Agent_System
```

```bash
.\venv\Scripts\activate
```

```bash
#python Resolvedor.py
py Resolvedor.py
```

### 6. When you're finished, you can deactivate the environment with a single command:
⚠️ **Do it for each terminal** ⚠️
```bash
deactivate
```

```bash
exit
```
