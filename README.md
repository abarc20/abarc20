# AbaRC-20

This script helps you mint AbaRC-20 tokens on the Aba blockchain

## Features

- Mints AbaRC-20 tokens with customizable parameters
- Uses the Abordinals library for Data URL encoding
- Interacts with the Aba node via RPC commands
- Supports optional dry-run mode to preview the minting process without submitting an actual transaction

## Requirements

- Python 3
- Abordinals library (copy chordinals.py over into this abarc20 dir for now)
- A configured Aba node with RPC access
- NFT wallet created, see Aba NFT Minting Docs (e.g. aba wallet nft create -n "abarc-20 nft wallet")
- The ticker being minted must have been deployed in a previous block and not yet minted out for the mint to be considered valid

## Usage

```
python abarc20_mint.py mint <ticker> --wallet-id <wallet_id> --address <address> --fee <fee> [--amt <amt>] [--dryrun]
```

### Arguments

```
    mint: Required command to execute (currently only supported option)
    <ticker>: Ticker symbol for the token (required)
    --wallet-id: Wallet ID of the NFT wallet in your Aba node (required, see aba wallet show)
    --address: Target address for the minted token to be sent to (required)
    --fee: Fee for the transaction in mojos (required)
    --amt (optional): Amount of tokens to mint (defaults to 1)
    --dryrun: Run in dry-run mode (no actual minting)
```

### Example

```
python abarc20_mint.py mint chordi --wallet-id 3 --address xch1qn98dq2xn27y... --fee 100000
```

### Output

In normal mode, the script will construct and display the Aba RPC command for minting the token. If successful, it will confirm the minting process.

In dry-run mode, the script will display the constructed Aba RPC command and the final mint JSON object in a human-readable format, but it won't actually mint the token.

### Additional Notes

This script utilizes temporary files to store intermediate JSON data during the minting process.

Ensure you have the necessary permissions to interact with the Aba node via RPC.

### References

[Chordiforge](https://www.chordiforge.com/)

[Chia NFT CLI Minting Guide](https://docs.chia.net/guides/nft-cli/)

### Disclaimer

This script is provided for informational purposes only. Please use it at your own risk and ensure you understand the implications of minting tokens on the Aba blockchain.
No warranty is provided.
