"""Command-line interface for tburundigeo package."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from tburundigeo.api.facade import (
    check_referential_integrity,
    count_communes,
    count_communes_in_province,
    count_provinces,
    count_quartiers,
    count_quartiers_in_zone,
    count_zones,
    count_zones_in_commune,
    export_to_csv,
    export_to_json,
    export_to_yaml,
    get_all_communes,
    get_all_provinces,
    get_all_quartiers,
    get_all_zones,
    get_communes_by_province,
    get_full_hierarchy,
    get_parent_commune,
    get_parent_province,
    get_parent_zone,
    get_quartiers_by_zone,
    get_statistics,
    get_summary,
    get_zones_by_commune,
    search_communes,
    search_provinces,
    search_quartiers,
    search_zones,
    # New detailed statistics functions
    get_province_statistics,
    get_commune_statistics,
    get_zone_statistics,
    get_all_provinces_statistics,
    get_all_communes_statistics,
    get_all_zones_statistics,
)
from tburundigeo.common.exceptions import (
    CommuneNotFoundError,
    ProvinceNotFoundError,
    ZoneNotFoundError,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="tburundigeo",
        description="Command-line interface for Burundi administrative divisions data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tburundigeo provinces list
  tburundigeo communes list --province BI-PR-01
  tburundigeo zones list --commune BI-CO-01-01
  tburundigeo quartiers list --zone BI-ZO-01-01-01
  tburundigeo search --query "Bujumbura" --level provinces
  tburundigeo stats
  tburundigeo export --format json --output burundi.json
  tburundigeo hierarchy --province BI-PR-01
  tburundigeo validate
  tburundigeo detailed-stats province BI-PR-01
  tburundigeo detailed-stats commune BI-CO-01-01
  tburundigeo detailed-stats zone BI-ZO-01-01-01
  tburundigeo detailed-stats all-provinces --format json
  tburundigeo detailed-stats all-communes
  tburundigeo detailed-stats all-zones
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Provinces commands
    provinces_parser = subparsers.add_parser("provinces", help="Province operations")
    provinces_subparsers = provinces_parser.add_subparsers(dest="provinces_command")
    
    provinces_list = provinces_subparsers.add_parser("list", help="List all provinces")
    provinces_list.add_argument("--with-capitals", action="store_true", help="Include capitals in output")
    provinces_list.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    provinces_search = provinces_subparsers.add_parser("search", help="Search provinces")
    provinces_search.add_argument("query", help="Search query")
    provinces_search.add_argument("--by", choices=["name", "code"], default="name", help="Search by field")
    
    # Communes commands
    communes_parser = subparsers.add_parser("communes", help="Commune operations")
    communes_subparsers = communes_parser.add_subparsers(dest="communes_command")
    
    communes_list = communes_subparsers.add_parser("list", help="List communes")
    communes_list.add_argument("--province", help="Filter by province code")
    communes_list.add_argument("--with-capitals", action="store_true", help="Include capitals in output")
    communes_list.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    communes_search = communes_subparsers.add_parser("search", help="Search communes")
    communes_search.add_argument("query", help="Search query")
    communes_search.add_argument("--by", choices=["name", "capital", "code"], default="name", help="Search by field")
    
    # Zones commands
    zones_parser = subparsers.add_parser("zones", help="Zone operations")
    zones_subparsers = zones_parser.add_subparsers(dest="zones_command")
    
    zones_list = zones_subparsers.add_parser("list", help="List zones")
    zones_list.add_argument("--commune", help="Filter by commune code")
    zones_list.add_argument("--with-chief-towns", action="store_true", help="Include chief towns in output")
    zones_list.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    zones_search = zones_subparsers.add_parser("search", help="Search zones")
    zones_search.add_argument("query", help="Search query")
    zones_search.add_argument("--by", choices=["name", "code"], default="name", help="Search by field")
    
    # Quartiers commands
    quartiers_parser = subparsers.add_parser("quartiers", help="Quartier operations")
    quartiers_subparsers = quartiers_parser.add_subparsers(dest="quartiers_command")
    
    quartiers_list = quartiers_subparsers.add_parser("list", help="List quartiers")
    quartiers_list.add_argument("--zone", help="Filter by zone code")
    quartiers_list.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    quartiers_search = quartiers_subparsers.add_parser("search", help="Search quartiers")
    quartiers_search.add_argument("query", help="Search query")
    quartiers_search.add_argument("--by", choices=["name", "code"], default="name", help="Search by field")
    
    # Search command (global search)
    search_parser = subparsers.add_parser("search", help="Global search across all levels")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--level", choices=["provinces", "communes", "zones", "quartiers", "all"], default="all", help="Search level")
    search_parser.add_argument("--by", choices=["name", "code"], default="name", help="Search by field")
    
    # Statistics command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument("--detailed", action="store_true", help="Show detailed statistics")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export data")
    export_parser.add_argument("--format", choices=["json", "csv", "yaml"], required=True, help="Export format")
    export_parser.add_argument("--output", help="Output file path (default: stdout)")
    export_parser.add_argument("--entity", choices=["provinces", "communes", "zones", "quartiers"], help="Entity type for CSV export")
    export_parser.add_argument("--hierarchy", action="store_true", help="Include hierarchy in JSON/YAML export")
    
    # Hierarchy command
    hierarchy_parser = subparsers.add_parser("hierarchy", help="Show hierarchy information")
    hierarchy_parser.add_argument("--province", help="Show hierarchy for specific province")
    hierarchy_parser.add_argument("--format", choices=["tree", "json"], default="tree", help="Output format")
    
    # Parent commands
    parent_parser = subparsers.add_parser("parent", help="Find parent of an entity")
    parent_parser.add_argument("code", help="Entity code")
    parent_parser.add_argument("--level", choices=["province", "commune", "zone"], help="Expected level of entity")
    
    # Validation command
    validate_parser = subparsers.add_parser("validate", help="Validate data integrity")
    validate_parser.add_argument("--detailed", action="store_true", help="Show detailed validation report")
    
    # Detailed statistics commands
    stats_parser = subparsers.add_parser("detailed-stats", help="Show detailed statistics for administrative entities")
    stats_subparsers = stats_parser.add_subparsers(dest="stats_command", help="Statistics commands")
    
    # Province statistics
    province_stats_parser = stats_subparsers.add_parser("province", help="Statistics for a specific province")
    province_stats_parser.add_argument("code", help="Province code")
    province_stats_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    # Commune statistics  
    commune_stats_parser = stats_subparsers.add_parser("commune", help="Statistics for a specific commune")
    commune_stats_parser.add_argument("code", help="Commune code")
    commune_stats_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    # Zone statistics
    zone_stats_parser = stats_subparsers.add_parser("zone", help="Statistics for a specific zone")
    zone_stats_parser.add_argument("code", help="Zone code")
    zone_stats_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    # All provinces statistics
    all_provinces_stats_parser = stats_subparsers.add_parser("all-provinces", help="Statistics for all provinces")
    all_provinces_stats_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    # All communes statistics
    all_communes_stats_parser = stats_subparsers.add_parser("all-communes", help="Statistics for all communes")
    all_communes_stats_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    # All zones statistics
    all_zones_stats_parser = stats_subparsers.add_parser("all-zones", help="Statistics for all zones")
    all_zones_stats_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    return parser


def format_table(data, headers):
    """Format data as a simple table."""
    if not data:
        return "No results found."
    
    # Convert data to list of lists
    if hasattr(data[0], '__dict__'):
        # Dataclass objects
        rows = []
        for item in data:
            row = []
            for header in headers:
                value = getattr(item, header, "")
                row.append(str(value))
            rows.append(row)
    else:
        # Dictionary objects
        rows = []
        for item in data:
            row = []
            for header in headers:
                value = item.get(header, "")
                row.append(str(value))
            rows.append(row)
    
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))
    
    # Build table
    lines = []
    
    # Header
    header_line = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))
    lines.append(header_line)
    lines.append("-" * len(header_line))
    
    # Data rows
    for row in rows:
        line = " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row))
        lines.append(line)
    
    return "\n".join(lines)


def handle_provinces_command(args):
    """Handle provinces commands."""
    if args.provinces_command == "list":
        provinces = get_all_provinces()
        if args.format == "json":
            if args.with_capitals:
                print(json.dumps([{"code": p.code, "name": p.name, "capital": p.capital} for p in provinces], indent=2, ensure_ascii=False))
            else:
                print(json.dumps([{"code": p.code, "name": p.name} for p in provinces], indent=2, ensure_ascii=False))
        else:
            print(format_table(provinces, ["code", "name", "capital"] if args.with_capitals else ["code", "name"]))
    
    elif args.provinces_command == "search":
        results = search_provinces(args.query, args.by)
        if args.format == "json":
            print(json.dumps([{"code": p.code, "name": p.name} for p in results], indent=2, ensure_ascii=False))
        else:
            print(format_table(results, ["code", "name"]))


def handle_communes_command(args):
    """Handle communes commands."""
    if args.province:
        communes = get_communes_by_province(args.province)
    else:
        communes = get_all_communes()
        
    if args.format == "json":
        if args.with_capitals:
            print(json.dumps([{"code": c.code, "name": c.name, "capital": c.capital, "province_code": c.province_code} for c in communes], indent=2, ensure_ascii=False))
        else:
            print(json.dumps([{"code": c.code, "name": c.name, "province_code": c.province_code} for c in communes], indent=2, ensure_ascii=False))
    else:
        print(format_table(communes, ["code", "name", "capital", "province_code"] if args.with_capitals else ["code", "name", "province_code"]))


def handle_zones_command(args):
    """Handle zones commands."""
    if args.zones_command == "list":
        if args.commune:
            zones = get_zones_by_commune(args.commune)
        else:
            zones = get_all_zones()
        
        if args.format == "json":
            if args.with_chief_towns:
                print(json.dumps([{"code": z.code, "name": z.name, "chief_town": z.chief_town, "commune_code": z.commune_code} for z in zones], indent=2, ensure_ascii=False))
            else:
                print(json.dumps([{"code": z.code, "name": z.name, "commune_code": z.commune_code} for z in zones], indent=2, ensure_ascii=False))
        else:
            print(format_table(zones, ["code", "name", "chief_town", "commune_code"] if args.with_chief_towns else ["code", "name", "commune_code"]))
    
    elif args.zones_command == "search":
        results = search_zones(args.query, args.by)
        if args.format == "json":
            print(json.dumps([{"code": z.code, "name": z.name, "commune_code": z.commune_code} for z in results], indent=2, ensure_ascii=False))
        else:
            print(format_table(results, ["code", "name", "commune_code"]))


def handle_quartiers_command(args):
    """Handle quartiers commands."""
    if args.quartiers_command == "list":
        if args.zone:
            quartiers = get_quartiers_by_zone(args.zone)
        else:
            quartiers = get_all_quartiers()
        
        if args.format == "json":
            print(json.dumps([{"code": q.code, "name": q.name, "zone_code": q.zone_code} for q in quartiers], indent=2, ensure_ascii=False))
        else:
            print(format_table(quartiers, ["code", "name", "zone_code"]))
    
    elif args.quartiers_command == "search":
        results = search_quartiers(args.query, args.by)
        if args.format == "json":
            print(json.dumps([{"code": q.code, "name": q.name, "zone_code": q.zone_code} for q in results], indent=2, ensure_ascii=False))
        else:
            print(format_table(results, ["code", "name", "zone_code"]))


def handle_search_command(args):
    """Handle global search command."""
    results = {}
    
    if args.level == "all" or args.level == "provinces":
        results["provinces"] = search_provinces(args.query, args.by)
    
    if args.level == "all" or args.level == "communes":
        results["communes"] = search_communes(args.query, args.by)
    
    if args.level == "all" or args.level == "zones":
        results["zones"] = search_zones(args.query, args.by)
    
    if args.level == "all" or args.level == "quartiers":
        results["quartiers"] = search_quartiers(args.query, args.by)
    
    print(json.dumps({
        "query": args.query,
        "results": {
            level: [{"code": item.code, "name": item.name} for item in items]
            for level, items in results.items()
        }
    }, indent=2, ensure_ascii=False))


def handle_stats_command(args):
    """Handle statistics command."""
    if args.detailed:
        stats = get_statistics()
    else:
        stats = {"summary": get_summary()}
    
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def handle_export_command(args):
    """Handle export command."""
    if args.format == "json":
        data = export_to_json(args.hierarchy)
    elif args.format == "yaml":
        data = export_to_yaml(args.hierarchy)
    elif args.format == "csv":
        if not args.entity:
            print("Error: --entity is required for CSV export", file=sys.stderr)
            sys.exit(1)
        data = export_to_csv(args.entity)
    else:
        print(f"Error: Unsupported format {args.format}", file=sys.stderr)
        sys.exit(1)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(data, encoding='utf-8')
        print(f"Data exported to {output_path}")
    else:
        print(data)


def handle_hierarchy_command(args):
    """Handle hierarchy command."""
    if args.province:
        # Show hierarchy for specific province
        hierarchy = get_full_hierarchy()
        if args.province in hierarchy:
            province_data = hierarchy[args.province]
            if args.format == "json":
                print(json.dumps(province_data, indent=2, ensure_ascii=False))
            else:
                print(f"Province: {province_data['name']} ({province_data['code']})")
                for commune_code, commune_data in province_data['communes'].items():
                    print(f"  Commune: {commune_data['name']} ({commune_data['code']})")
                    for zone_code, zone_data in commune_data['zones'].items():
                        print(f"    Zone: {zone_data['name']} ({zone_data['code']})")
                        for quartier_code, quartier_data in zone_data['quartiers'].items():
                            print(f"      Quartier: {quartier_data['name']} ({quartier_data['code']})")
        else:
            print(f"Province {args.province} not found", file=sys.stderr)
            sys.exit(1)
    else:
        # Show full hierarchy
        hierarchy = get_full_hierarchy()
        if args.format == "json":
            print(json.dumps(hierarchy, indent=2, ensure_ascii=False))
        else:
            for province_code, province_data in hierarchy.items():
                print(f"Province: {province_data['name']} ({province_data['code']})")
                for commune_code, commune_data in province_data['communes'].items():
                    print(f"  Commune: {commune_data['name']} ({commune_data['code']})")
                    for zone_code, zone_data in commune_data['zones'].items():
                        print(f"    Zone: {zone_data['name']} ({zone_code['code']})")
                        for quartier_code, quartier_data in zone_data['quartiers'].items():
                            print(f"      Quartier: {quartier_data['name']} ({quartier_data['code']})")


def handle_parent_command(args):
    """Handle parent command."""
    try:
        if args.level == "province" or not args.level:
            # Try to find parent province
            parent = get_parent_province(args.code)
            if parent:
                print(f"Parent province: {parent.name} ({parent.code})")
                return
        
        if args.level == "commune" or not args.level:
            # Try to find parent commune
            parent = get_parent_commune(args.code)
            if parent:
                print(f"Parent commune: {parent.name} ({parent.code})")
                return
        
        if args.level == "zone" or not args.level:
            # Try to find parent zone
            parent = get_parent_zone(args.code)
            if parent:
                print(f"Parent zone: {parent.name} ({parent.code})")
                return
        
        print(f"No parent found for {args.code}", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"Error finding parent for {args.code}: {e}", file=sys.stderr)
        sys.exit(1)


def handle_validate_command(args):
    """Handle validation command."""
    if args.detailed:
        # Get detailed validation report
        try:
            # This would require access to validation service
            # For now, just do basic referential integrity check
            errors = check_referential_integrity()
            
            total_errors = sum(len(error_list) for error_list in errors.values())
            
            if total_errors == 0:
                print("✅ All validation checks passed!")
            else:
                print(f"❌ Found {total_errors} validation errors:")
                for error_type, error_list in errors.items():
                    if error_list:
                        print(f"\n{error_type}:")
                        for error in error_list:
                            print(f"  - {error}")
        except Exception as e:
            print(f"Error during validation: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Quick validation
        errors = check_referential_integrity()
        total_errors = sum(len(error_list) for error_list in errors.values())
        
        if total_errors == 0:
            print("✅ Referential integrity check passed!")
        else:
            print(f"❌ Found {total_errors} referential integrity errors")
            sys.exit(1)


def handle_detailed_stats_command(args):
    """Handle detailed statistics commands."""
    try:
        if args.stats_command == "province":
            stats = get_province_statistics(args.code)
            if args.format == "json":
                print(json.dumps(stats, indent=2, ensure_ascii=False))
            else:
                print(f"Province: {stats['province_name']} ({stats['province_code']})")
                print(f"  Communes: {stats['communes_count']}")
                print(f"  Zones: {stats['zones_count']}")
                print(f"  Quartiers: {stats['quartiers_count']}")
        
        elif args.stats_command == "commune":
            stats = get_commune_statistics(args.code)
            if args.format == "json":
                print(json.dumps(stats, indent=2, ensure_ascii=False))
            else:
                print(f"Commune: {stats['commune_name']} ({stats['commune_code']})")
                print(f"  Province: {stats['province_name']} ({stats['province_code']})")
                print(f"  Zones: {stats['zones_count']}")
                print(f"  Quartiers: {stats['quartiers_count']}")
        
        elif args.stats_command == "zone":
            stats = get_zone_statistics(args.code)
            if args.format == "json":
                print(json.dumps(stats, indent=2, ensure_ascii=False))
            else:
                print(f"Zone: {stats['zone_name']} ({stats['zone_code']})")
                print(f"  Commune: {stats['commune_name']} ({stats['commune_code']})")
                print(f"  Province: {stats['province_name']} ({stats['province_code']})")
                print(f"  Quartiers: {stats['quartiers_count']}")
        
        elif args.stats_command == "all-provinces":
            stats_list = get_all_provinces_statistics()
            if args.format == "json":
                print(json.dumps(stats_list, indent=2, ensure_ascii=False))
            else:
                headers = ["province_code", "province_name", "communes_count", "zones_count", "quartiers_count"]
                print(format_table(stats_list, headers))
        
        elif args.stats_command == "all-communes":
            stats_list = get_all_communes_statistics()
            if args.format == "json":
                print(json.dumps(stats_list, indent=2, ensure_ascii=False))
            else:
                headers = ["commune_code", "commune_name", "province_code", "province_name", "zones_count", "quartiers_count"]
                print(format_table(stats_list, headers))
        
        elif args.stats_command == "all-zones":
            stats_list = get_all_zones_statistics()
            if args.format == "json":
                print(json.dumps(stats_list, indent=2, ensure_ascii=False))
            else:
                headers = ["zone_code", "zone_name", "commune_code", "commune_name", "province_code", "province_name", "quartiers_count"]
                print(format_table(stats_list, headers))
        
        else:
            print("Please specify a statistics command. Use --help for options.", file=sys.stderr)
            return 1
    
    except (ProvinceNotFoundError, CommuneNotFoundError, ZoneNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error getting statistics: {e}", file=sys.stderr)
        return 1


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "provinces":
            handle_provinces_command(args)
        elif args.command == "communes":
            handle_communes_command(args)
        elif args.command == "zones":
            handle_zones_command(args)
        elif args.command == "quartiers":
            handle_quartiers_command(args)
        elif args.command == "search":
            handle_search_command(args)
        elif args.command == "stats":
            handle_stats_command(args)
        elif args.command == "export":
            handle_export_command(args)
        elif args.command == "hierarchy":
            handle_hierarchy_command(args)
        elif args.command == "parent":
            handle_parent_command(args)
        elif args.command == "validate":
            handle_validate_command(args)
        elif args.command == "detailed-stats":
            handle_detailed_stats_command(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1
        
        return 0
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
