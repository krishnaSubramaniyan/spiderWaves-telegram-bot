from crypto import CryptoEngine

key = CryptoEngine.generate_key(32)
crypto_eng = CryptoEngine(key,12)
msg = crypto_eng.encrypt("hello world")
print(f"encrypt = {msg}")
print(f"decrypt = {crypto_eng.decrypt(msg)}")
