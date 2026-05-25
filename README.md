
# 🚀 GHCP Proxy: Unrestricted Premium Access (Invite Only)

### The Problem
If you are doing serious engineering, you already know the truth: standard web subscriptions (ChatGPT Plus, Claude Pro) secretly serve heavily quantized, degraded models to save compute. If you want true, unquantized, high-precision AI, you need API-level access. But API costs scale out of control, and standard GitHub Copilot (GHCP) strictly rate-limits its Premium models. 

### The Solution (The Exploit)
I discovered a backend exploit in GHCP's routing architecture about **1.5 years ago**, and I have been using it successfully ever since. It allows a Pro+ account to bypass the standard Premium request quota, effectively unlocking continuous premium responses. 

I have built a custom proxy server that securely implements this exploit. **I am not open-sourcing the server code.** If everyone starts using it, GH will catch on and kill it, causing the exact same situation that happened recently when GH abandoned PR-based auth and forced token-based auth to stop abusers. 

And if you want the blunt truth: if I open-source the proxy, people will just run it themselves, and nobody will share an auth key with me so I can use it too. 

### The Deal 
I need access to a Pro+ account to route through the proxy, and you want to eliminate your premium request limits without paying for raw API tokens. We share the proxy.

* You use the open-source authenticator in this repo to securely get your GHCP Auth Token.
* You send the token to me.
* I add it to the proxy and give you a custom API endpoint for your IDE/client.

**The Result:** You will no longer face those annoying Premium request rate limits. You can just code naturally without constantly hitting a wall. 

### 🛑 The "No Vibe Coders" Rule (Fair Use)
While there are no arbitrary request limits, I enforce a firm processing cap on the server to keep out abusers. **I strictly do not want "vibe coders" on this proxy.** 

Vibe coders don't even need this proxy anyway—they can just leave long-running AI sessions open and let it slowly generate junk code. This proxy is for disciplined engineers who need instant, high-quality, unquantized answers for deep architectural logic and debugging. 

---

### 🔒 Security: Addressing the GH Authorization Warning

I know running an authenticator script sounds sketchy. When the GH authorization page opens, you will see a generic yellow warning: *"Make sure you trust this device as it will get access to your account."* 

**Here is exactly why you don't need to worry about that:**
1. **It's boilerplate:** That is GitHub's default warning text for *every* OAuth application. 
2. **Check the Scopes:** Look directly below that warning at the actual permissions requested. It is explicitly the **"GitHub Copilot Plugin by GitHub"**. It *only* requests to verify your identity. **It does NOT request the `repo` scope.** This means the token literally cannot read your private repositories, view your code, or change your settings.
3. **The Kill Switch:** You have total control. If you ever want out, you just use the exact same authenticator tool to log out. The moment you click log out, the auth key is permanently invalidated on GH's end, and my proxy instantly loses access. 
4. **Open Source Check:** Do not trust me—trust the code. Read `authenticator.py` before you run it. It only handles the Copilot OAuth handshake.

---

### How to Join

1. **Audit the Authenticator:** Check the code in this repo to verify it is safe.
2. **Run it:** Execute the script. The GH authorization page will open.
3. **Copy the Token:** The terminal will output your isolated Auth Token.
4. **Send it:** Send me the token securely via [Insert Contact Method: e.g., Telegram / Session / ProtonMail].
5. **Connect:** I will reply with your dedicated Proxy Endpoint URL and instructions on how to route your IDE/WebUI through it.

---
*Note: This is strictly for high-level research and development purposes.*

**🚨 EDIT: 4 seats remaining, 1 seat taken. DM me if you want in.**
