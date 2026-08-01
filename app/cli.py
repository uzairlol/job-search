import argparse

from app.services.cycle_runner import CycleRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local job acquisition workflow")
    parser.add_argument("--focus", default="remote ai ml research")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--artifact-root", default="storage/artifacts")
    args = parser.parse_args()

    runner = CycleRunner(profile_dir="user_profile", artifact_root=args.artifact_root)
    result = runner.run_once(focus_terms=args.focus, company_limit=args.limit)
    print(result)


if __name__ == "__main__":
    main()
