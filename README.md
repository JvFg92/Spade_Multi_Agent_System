## Setting up Local Host

### **On Linux 🐧:**
**On Linux 🐧:**
```bash
sudo apt update
```

```bash
sudo apt install ejabberd
```

```bash
sudo ejabberdctl register "your_user" localhost "your_password"
```

### **On Windows 🪟:**

1. **Check if Java is Installed**:
   ```cmd
   java -version
   ```
   If installed, you’ll see a version like `java version "1.8.0_281"`. If not, proceed.

2. **Download and Install Java**:
   - Visit [Oracle Java Downloads](https://www.oracle.com/java/technologies/javase-downloads.html) or [AdoptOpenJDK](https://adoptopenjdk.net/).
   - Download JDK 8 or 11 for Windows (e.g., `.exe` installer).
   - Run the installer, following the prompts.

3. **Set JAVA_HOME**:
   - Right-click **This PC** > **Properties** > **Advanced system settings** > **Environment Variables**.
   - Under **System Variables**, click **New**:
     - **Variable name**: `JAVA_HOME`
     - **Variable value**: Path to JDK (e.g., `C:\Program Files\Java\jdk1.8.0_281`).
   - Edit **Path** variable, add: `%JAVA_HOME%\bin`.
   - Verify:
     ```cmd
     java -version
     ```

*Openfire is an open-source XMPP server used for local agent communication.*

1. **Download Openfire**:
   - Go to [Openfire Downloads](https://www.igniterealtime.org/projects/openfire/).
   - Download the latest Windows installer (e.g., `openfire_4_8_0.exe`).

2. **Install Openfire**:
   - Run the installer.
   - Install to a directory (e.g., `C:\Program Files\Openfire`).
   - Accept default settings and install as a service.

3. **Start Openfire**:
   - Openfire starts automatically post-installation. If not:
     - Open **Services** (`Win + R`, type `services.msc`).
     - Find **Openfire**, right-click, and select **Start**.
     - Or run manually:
       ```cmd
       C:\Program Files\Openfire\bin\openfire.exe
       ```

4. **Configure Openfire**:
   - Open a browser and go to `http://localhost:9090`.
   - Complete the setup wizard:
     - **Language**: Choose English (or preferred language).
     - **Server Settings**: Use default (`localhost` domain, ports `5222` for clients, `9090` for admin console).
     - **Database**: Select **Embedded Database** for simplicity.
     - **Profile Settings**: Use default (store users in database).
     - **Admin Account**: Set email and password (e.g., `admin@localhost`, password: `admin123`).

**Step 3: Create XMPP Users**

The agents require users `"your_user"@localhost` and `"other_user"@localhost` with password `"your_password"`.

1. **Log into Openfire Admin Console**:
   - Navigate to `http://localhost:9090`.
   - Log in with admin credentials (e.g., `admin@localhost`, `admin123`).

2. **Create User `"your_user"@localhost`**:
   - Go to **Users/Groups** > **Create New User**.
   - Enter:
     - **Username**: `"your_user"@localhost`
     - **Name**: (optional, e.g., Gerador)
     - **Email**: (optional)
     - **Password**: `"your_password"`
     - **Confirm Password**: `"your_password"`
   - Click **Create**.

3. **Create User `"other_user"@localhost`**:
   - Repeat:
     - **Username**: `"other_user"@localhost`
     - **Name**: (optional, e.g., Resolvedor)
     - **Email**: (optional)
     - **Password**: `"your_password"`
     - **Confirm Password**: `"your_password"`
   - Click **Create**.

4. **Verify Users**:
   - Go to **Users/Groups** > **User Summary** and confirm `"your_user"` and `"other_user"` are listed.


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
⚠️ **Open a Terminal** ⚠️

**On Linux 🐧:**
```bash
cd my_spade_project
```

```bash
source venv/bin/activate
```

```bash
cd Spade_Multi_Agent_System
```

```bash
python3 Gerador.py
```

**On Windows 🪟:**
```bash
cd my_spade_project
```

```bash
.\venv\Scripts\activate
```

```bash
cd Spade_Multi_Agent_System
```

```bash
#python Gerador.py
py Gerador.py
```

**Solver:**
⚠️ **Open another Terminal** ⚠️

**On Linux 🐧:**
```bash
cd my_spade_project
```

```bash
source venv/bin/activate
```

```bash
cd Spade_Multi_Agent_System
```

```bash
python3 Resolvedor.py
```

**On Windows 🪟:**
```bash
cd my_spade_project
```

```bash
.\venv\Scripts\activate
```

```bash
cd Spade_Multi_Agent_System
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
