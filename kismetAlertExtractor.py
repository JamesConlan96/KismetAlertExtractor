#!/usr/bin/env python


import argparse
from datetime import datetime
import json
from pathlib import Path
import sqlite3
import sys
from tabulate import tabulate, tabulate_formats


def genArgParser() -> argparse.ArgumentParser:
    """Generates a CLI argument parser
    @return: CLI argument parser object
    """
    defaultFields = [
        "kismet.alert.timestamp",
        "kismet.alert.class",
        "kismet.alert.header",
        "kismet.alert.text",
        "kismet.alert.severity",
        "kismet.alert.source_mac",
        "kismet.alert.dest_mac",
        "kismet.alert.frequency",
        "kismet.alert.channel",
    ]
    parser = argparse.ArgumentParser(description="Kismet alert extractor",
                                     prog=str(Path(__file__).name))
    parser.add_argument("-f", "--fields", nargs="+", metavar="FIELD",
                        choices=list(kismetFields.keys()),
                        default=defaultFields,
                        help="kismet alert fields to include in output" +
                        f"(Default: '{', '.join(defaultFields)}')")
    parser.add_argument("-i", "--inputFiles", nargs="+", type=Path,
                        metavar="FILE", action="store",
                        help="kismet file(s) to extract alerts from")
    parser.add_argument("-l", "--listFields", action="store_true",
                        help="list supported kismet alert fields")
    parser.add_argument("-o", "--outputFile", type=Path, action="store",
                        metavar="FILE", help="file to save alerts to")
    parser.add_argument('-s', '--style', choices=tabulate_formats,
                        help="style for output tables (default: github)",
                        default="github")
    return parser

def _yesNo(prompt: str) -> bool:
    """Prompts the user for a yes/no response
    @param prompt: Prompt to display to the user
    @return: True if yes, False if no
    """
    yn = input(f"{prompt} (y/n): ")
    if yn.lower() == 'y':
        return True
    elif yn.lower() == 'n':
        return False
    else:
        return _yesNo(prompt)

def _validateArgs(args: argparse.Namespace) -> None:
    """Validates provided CLI arguments
    @param args: Argparse namespace containing parsed CLI arguments
    """
    if args.listFields:
        for field in kismetFields.keys():
            print(field)
        sys.exit()
    if not args.inputFiles:
        sys.exit("The following argument is required: -i/--inputFiles")
    if not args.outputFile:
        sys.exit("The following argument is required: -o/--outputFile")
    for inFile in args.inputFiles:
        if not inFile.exists:
            sys.exit(f"Input file '{inFile}' does not exist")
    if args.outputFile.exists():
        if not _yesNo(f"Output file '{args.outputFile}' exists, overwrite it?"):
            sys.exit()
        try:
            args.outputFile.open("w").close()
        except:
            sys.exit(f"Could not write to output file '{args.outputFile}'")

def getAlerts(kismetFile: Path) -> list:
    """Extracts a list of alerts from a given .kismet file"""
    print(f"Extracting alerts from '{kismetFile}'...")
    con = sqlite3.connect(kismetFile)
    cur = con.cursor()
    alerts = []
    for row in cur.execute("SELECT json FROM alerts;"):
        data = json.loads(row[0])
        alerts.append(data)
    alerts.sort(key=lambda x: x["kismet.alert.timestamp"])
    return alerts

def _procTime(timestamp: float) -> str:
    """Processes a timestamp to make it human-readable
    @param timestamp: Timestamp to process
    @retun: Human-readable string representation of the processed timestamp
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d %H:%M:%S")

def _procLoc(locData: dict) -> str:
    """Processes kismet location data to make it human-readable
    @param locData: Kismet location data to process
    @return: Human-readable string representation of the processed location data
    """
    return ", ".join(str(x) for x in locData["kismet.common.location.geopoint"])

def report(alerts: list[dict], fields: list[str], style: str, outFile: Path
           ) -> None:
    """Reports on alerts
    @param alerts: A list of alert objects to report on
    @param fields: A list of kismet fields to include when reporting
    @param style: Style to use when generating tables
    @param outFile: File to save output to
    """
    print("Generating report...")
    headings = [kismetFields[field][0] for field in fields]
    rows = []
    for alert in alerts:
        row = []
        for field in fields:
            if kismetFields[field][1] is not None:
                val = kismetFields[field][1](alert[field])
            else:
                val = alert[field]
            val = "N/A" if val == "" else val
            row.append(val)
        rows.append(row)
    with outFile.open("w") as f:
        f.write(tabulate(rows, headings, style))

def main(cliArgs: list = sys.argv[1:]) -> None:
    """Main method
    @param cliArgs: CLI arguments to use
    """
    global kismetFields
    # Format = kismet_field_name: (output_heading, formatting_function/None)
    kismetFields = {
            "kismet.alert.device_key": ("Device Key", None),
            "kismet.alert.header": ("Title", None),
            "kismet.alert.class": ("Category", None),
            "kismet.alert.hash": ("Hash", None),
            "kismet.alert.severity": ("Severity", None),
            "kismet.alert.phy_id": ("Physical ID", None),
            "kismet.alert.timestamp": ("Time", _procTime),
            "kismet.alert.transmitter_mac": ("Transmitter MAC", None),
            "kismet.alert.source_mac": ("Source MAC", None),
            "kismet.alert.dest_mac": ("Destination MAC", None),
            "kismet.alert.other_mac": ("Other MAC", None),
            "kismet.alert.channel": ("Channel", None),
            "kismet.alert.frequency": ("Frequency", None),
            "kismet.alert.text": ("Description", None),
            "kismet.alert.location": ("Location", _procLoc)
    }
    if len(cliArgs) < 1:
        genArgParser().print_usage()
        sys.exit()
    args = genArgParser().parse_args(cliArgs)
    _validateArgs(args)
    alerts = []
    for kismetFile in args.inputFiles:
        alerts += getAlerts(kismetFile)
    report(alerts, args.fields, args.style, args.outputFile)


if __name__ == "__main__":
    main()
