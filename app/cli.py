import argparse

from app.services.workflow import LocalJobWorkflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local job acquisition workflow")
    parser.add_argument("--role", default="Machine Learning Engineer")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    workflow = LocalJobWorkflow(profile_dir="user_profile")
    workflow.run(target_role=args.role, company_limit=args.limit)


if __name__ == "__main__":
    main()
