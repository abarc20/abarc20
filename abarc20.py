"""
Script for minting a AbaRC-20 token on the Aba blockchain.

This script takes various arguments to configure the minting process,
including the ticker symbol, wallet ID, target address, fee, and optional
amount and fingerprint. It uses the `chordinals` library for URI encoding
and interacts with the Aba node via RPC commands.
"""

import json
import hashlib
import subprocess
import tempfile
import argparse
import chordinals


def calculate_sha256_hash(input_filename):
    """Calculates the SHA-256 hash of a file's content.

    Args:
      input_filename: The path to the file to hash.

    Returns:
      A string containing the hexadecimal representation of the hash.
    """
    with open(input_filename, 'rb') as f:
        file_content = f.read()
        sha256_hash = hashlib.sha256(file_content).hexdigest()
    return sha256_hash


def main():
    """Parses command-line arguments and performs the AbaRC-20 token minting process.
    """
    parser = argparse.ArgumentParser(
        description="Mint an AbaRC-20 token on the Aba blockchain")
    parser.add_argument("command", type=str, choices=[
                        "mint"], help="Command to execute, only mint command supported currently")
    parser.add_argument("ticker", type=str,
                        help="Ticker symbol for the token")
    parser.add_argument("--wallet-id", type=int,
                        required=True, help="Wallet ID (optional)")
    parser.add_argument("--address", type=str, required=True,
                        help="Target address for the token")
    parser.add_argument("--fee", type=int, required=True, help="Fee in mojos")
    parser.add_argument("--amt", type=int,
                        help="Amount of tokens to mint (optional)")
    parser.add_argument("--dryrun", action='store_true',
                        help="Run without generating & sending transaction to the mempool")
    args = parser.parse_args()
    # print("Usage: python3 abarc20.py mint ticker --wallet-id 3 --address to_address --fee mojos
    #  --amt 10 (amt is optional)")
    if args.command != "mint":
        print("Invalid command. Please use 'mint'")
        exit()
    # if args.fee < 1:
    #    raise ValueError("Fee must be at least 1 mojo")

    ticker = args.ticker

    # 1. Encode urifile and calculate its hash

    with open("abarc-20-mint-uri-template.json", "r") as f:
        uri_json = json.load(f)

    # In metadata_json, 1) replace name w/ ticker, 2) data.tick with ticker, 3) if amt
    # value is given, then add data["amt"]=amt, 4) create temp file metadatafile w/ minimal
    #  whitespace for the json
    uri_json["tick"] = ticker
    if "amt" in args and args.amt is not None:
        uri_json["amt"] = args.amt
    # indent=4))
    print(json.dumps(uri_json, indent=None, separators=(',', ':')))

    # Create a temporary file for metadata JSON
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
        json.dump(uri_json, temp_file, indent=None, separators=(',', ':'))
        uri_file_path = temp_file.name
    uri_data_uri = chordinals.encode_for_data_url(uri_file_path)
    uri_hash = calculate_sha256_hash(uri_file_path)

    if "dryrun" in args:
        print(uri_data_uri)
        print(uri_hash)

    # 2. Create metadatafile.json using template and calculate its hash
    with open("abarc-20-mint-metadata-template.json", "r") as f:
        metadata_json = json.load(f)

    # In metadata_json, 1) replace name w/ ticker, 2) data.tick with ticker, 3) if amt
    # value is given, then add data["amt"]=amt, 4) create temp file metadatafile w/ minimal
    #  whitespace for the json
    metadata_json["name"] = ticker
    # metadata_json["data"]["tick"] = ticker
    # if "amt" in args and args.amt is not None:
    #    metadata_json["data"]["amt"] = args.amt
    # indent=4))
    print(json.dumps(metadata_json, indent=None, separators=(',', ':')))

    # Create a temporary file for metadata JSON
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
        json.dump(metadata_json, temp_file, indent=None, separators=(',', ':'))
        metadata_file_path = temp_file.name
    metadata_data_uri = chordinals.encode_for_data_url(metadata_file_path)
    metadata_hash = calculate_sha256_hash(metadata_file_path)

    if "dryrun" in args:
        print(metadata_data_uri)
        print(metadata_hash)

    # 3. Start creating the mint json file; Read template.json
    with open("abarc-20-mint-template.json", "r") as f:
        template_json = json.load(f)

    # 4. & 5. Replace values in template.json
    template_json["wallet_id"] = args.wallet_id
    template_json["target_address"] = args.address
    template_json["fee"] = args.fee
    template_json["uris"] = [uri_data_uri]
    template_json["hash"] = uri_hash
    template_json["meta_uris"] = [metadata_data_uri]
    template_json["meta_hash"] = metadata_hash

    # --- Create a temporary file with the final mint json ---
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
        json.dump(template_json, temp_file, indent=4)
        temp_file_path = temp_file.name

    # Construct the aba rpc command using the temporary file path
    command = f"aba rpc wallet nft_mint_nft -j {temp_file_path}"

    print(command)
    print(json.dumps(template_json, indent=4))
    # Run the command

    if not args.dryrun:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error minting NFT: {e}")
    else:
        print("Dry run mode: minting not executed.")


if __name__ == "__main__":
    main()
