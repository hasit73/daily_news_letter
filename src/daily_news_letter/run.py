from uuid import uuid4

from dotenv import load_dotenv


def main() -> None:
    # Load .env before importing the workflow so module-level config sees it.
    load_dotenv()

    from daily_news_letter.api import send_message
    from daily_news_letter.workflow import create_workflow

    graph = create_workflow()

    thread_config = {"configurable": {"thread_id": str(uuid4())}}
    response = graph.invoke({}, config=thread_config)

    for message_sections in response["output_messages"]:
        message = "\n\n".join(message_sections)
        resp = send_message(message)
        if not resp.ok:
            print("Error in sending msg : ", resp.json())


if __name__ == "__main__":
    main()
