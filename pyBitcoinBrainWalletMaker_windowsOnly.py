import os
import msvcrt
import qrcode_terminal

from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip39Languages,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

def generate_seed_phrase():
    """Generate a 12-word seed phrase."""
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    return mnemonic

def verify_seed_phrase(seed_phrase, lang=Bip39Languages.ENGLISH):
    """Verify the given seed phrase."""
    try:
        validator = Bip39MnemonicValidator(lang)
        validator.Validate(seed_phrase)
        return True
    except Exception as e:
        print("Error:", e)
        return False

def derive_keys(seed_phrase):
    """Derive private and public keys from the given seed phrase."""
    seed = Bip39SeedGenerator(seed_phrase).Generate()
    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    bip44_account = bip44_wallet.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    bip44_address = bip44_account.AddressIndex(0)

    private_key = bip44_address.PrivateKey().ToWif()
    address = bip44_address.PublicKey().ToAddress()

    return private_key, address

def print_keys(seed_phrase):
    """Print the private and public address derived from the given seed phrase."""
    private_key, public_key = derive_keys(seed_phrase)
    os.system("cls")  # Clear the terminal
    print("Random 12-word seed phrase - memorise or store these safely, full access hot wallet is created with this phrase\n\n") 
    print(seed_phrase)
    print("\n\nPrivate key:", private_key)
    print("Public Address:", public_key)
    print("\nPress the spacebar to randomly generate a new seed phrase\r")
    print("Press h for hot wallet qrcode - (Private Key) create a full access daily wallet, or use for cold wallet access\r")
    print("Press c for cold wallet qrcode - (Public Address) use to create a safe watch only wallet online, it can recieve funds only. REQUIRES the seed-phrase or private key(hot wallet) to access wallet and send transactions\r")
    print("Press x to hide qrcode\nPress q to quit.\r")   
    return private_key, public_key

def handle_key_event(key, seed_phrase):
    """Handle key events and perform the corresponding actions."""
    if key == b' ':
        seed_phrase = generate_seed_phrase()
        if verify_seed_phrase(seed_phrase):
            private_key, public_key = print_keys(seed_phrase)
            return seed_phrase
        else:
            print("The seed phrase is not valid.")
            return seed_phrase

    elif key == b'c':
        private_key, public_key = print_keys(seed_phrase)
        qrcode_terminal.draw(public_key)

    elif key == b'h':
        private_key, public_key = print_keys(seed_phrase)
        qrcode_terminal.draw(private_key)

    elif key == b'x':
        private_key, public_key = print_keys(seed_phrase)

    elif key == b'q':
        print("\nGoodbye!")
        return None

    return seed_phrase

def main():
    os.system("cls")  # Clear the terminal
    print("Press the spacebar to randomly generate a new seed phrase, or press 'q' to quit.")
    seed_phrase = generate_seed_phrase()

    while seed_phrase:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            seed_phrase = handle_key_event(key, seed_phrase)

if __name__ == "__main__":
    main()    