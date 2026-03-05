# name: Coleman Pagac
# date: 2026-03-04
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) -- if I don't change this, I agree to get 0 points.



import boto3


REGION = "us-east-1"
TABLE_NAME = "Games"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def print_game(game):
	title = game.get("Title", "Unknown Title")
	genre = game.get("Genre", "Unknown Genre")
	platform = game.get("Platform", "Unknown Platform")
	rating = game.get("Rating", "No rating")

	print(f"  Title   : {title}")
	print(f"  Genre   : {genre}")
	print(f"  Platform: {platform}")
	print(f"  Rating  : {rating}")
	print()


def create_game():
	title = input("Enter game title: ").strip()
	genre = input("Enter genre: ").strip()
	platform = input("Enter platform: ").strip()

	try:
		rating = int(input("Enter rating (integer): "))
	except Exception:
		print("error creating game")
		return

	if not title:
		print("Game title cannot be empty.")
		return

	table.put_item(
		Item={
			"Title": title,
			"Genre": genre,
			"Platform": platform,
			"Rating": rating,
		}
	)
	print(f"Created game: {title}")


def print_all_games():
	response = table.scan()
	items = response.get("Items", [])

	if not items:
		print("No games found.")
		return

	print(f"Found {len(items)} game(s):\n")
	for game in items:
		print_game(game)


def update_game():
	try:
		title = input("What is the game title? ").strip()
		rating = int(input("What is the new rating (integer)? "))

		if not title:
			print("Game title cannot be empty.")
			return

		table.update_item(
			Key={"Title": title},
			UpdateExpression="SET Rating = :r",
			ExpressionAttributeValues={":r": rating},
		)
		print(f"Updated rating for {title}")
	except Exception:
		print("error updating game")


def delete_game():
	title = input("What is the game title? ").strip()
	if not title:
		print("Game title cannot be empty.")
		return

	table.delete_item(Key={"Title": title})
	print(f"Deleted game: {title}")


def query_game():
	title = input("What is the game title? ").strip()
	if not title:
		print("Game title cannot be empty.")
		return

	response = table.get_item(Key={"Title": title})
	game = response.get("Item")

	if not game:
		print("Game not found.")
		return

	print("Game found:\n")
	print_game(game)


def print_menu():
	print("----------------------------")
	print("Press C: to CREATE a new game")
	print("Press R: to READ all games")
	print("Press U: to UPDATE a game rating")
	print("Press D: to DELETE a game")
	print("Press Q: to QUERY a game by title")
	print("Press X: to EXIT application")
	print("----------------------------")


def main():
	input_char = ""
	while input_char.upper() != "X":
		print_menu()
		input_char = input("Choice: ")
		if input_char.upper() == "C":
			create_game()
		elif input_char.upper() == "R":
			print_all_games()
		elif input_char.upper() == "U":
			update_game()
		elif input_char.upper() == "D":
			delete_game()
		elif input_char.upper() == "Q":
			query_game()
		elif input_char.upper() == "X":
			print("exiting...")
		else:
			print("Not a valid option. Try again.")


if __name__ == "__main__":
	main()
