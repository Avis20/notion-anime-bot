from notion.client import NotionClient

client = NotionClient(token_v2="3986a790b88a40f2724428b736b66a2274a7398468f4a98d5618a0f6242aa40e133cef75acfc2eefd03198f05f0344e0a2e0bbf839eb767532b4e72526c7c974e4f923baef9e5f643125ed4fa0f2")
page = client.get_block("https://www.notion.so/avis/trestts-e31cd48e31a348c8b9eac178aba894db")

print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
page.title = "The title has now changed, and has *live-updated* in the browser!"
print(page.image)
