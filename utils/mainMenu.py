from utils.mainAPI import malAPICheck
from utils.mainDatabase import Database

def viewWatchedList(user):

    print("\nYour watched shows:")

    if not user.watched_shows:
        print("You haven't added any shows yet.")

    else:
        for show in user.watched_shows:
            print(f"- {show.show_name} (Your rating: {show.personal_score})")

    input("Press Enter to go back to main menu...")

    return

def viewComments(user):
    db = Database()

    print("\nComments on your page:\n")

    db.cursor.execute("""
        SELECT pc.comment, u.username
        FROM software_architecture_profile_comments pc
        JOIN software_architecture_credentials u
            ON pc.user_id_commenter = u.id
        WHERE pc.user_id_profile = %s
    """, (user.id,))

    rows = db.cursor.fetchall()

    if not rows:
        print("No comments yet.")
        input("Press Enter to go back...")
        return

    # Print comments
    for comment_text, commenter_name in rows:
        print(f"{commenter_name}: {comment_text}")

    input("Press Enter to go back...")
    return

def commentOnSomeonesPage(currentUser):
    print("\nList of all users:")

    db = Database()
    db.cursor.execute(""" 
        SELECT id, username 
        FROM software_architecture_credentials
        WHERE id != %s
    """, (currentUser.id,))         # Get all users except the current user

    rows = db.cursor.fetchall()

    if not rows:
        print("No other users exist.")
        return

    # Display users in a numbered list
    for i, (user_id, username) in enumerate(rows, start=1):
        print(f"{i}. {username}")

    # Ask user to pick one
    choice = input("Enter the number of the user you want to comment on: ")

    try:
        index = int(choice) - 1
        selected_user_id, selected_username = rows[index]
    except:
        print("Invalid selection.")
        return

    # Ask for comment
    comment_text = input(f"Write your comment for {selected_username}: ")

    # Insert the comment
    db.cursor.execute("""
        INSERT INTO software_architecture_profile_comments (user_id_profile, user_id_commenter, comment)
        VALUES (%s, %s, %s)
    """, (selected_user_id, currentUser.id, comment_text))

    db.commit()

    print("Comment posted successfully!")
    input("Press Enter to go back to main menu...")

    return

def mainMenu(user):
    logicGate = True

    while logicGate:
        
        print(f'\nWelcome, {user.username}. What would you like to perform?')
        print(f'(1) --> Search for a show')
        print(f'(2) --> View Personal Watched List')
        print(f'(3) --> Comment on Someones Page')
        print(f'(4) --> View Comments on My Page')
        print(f'(5) --> View Badges')
        print(f'(6) --> Log Out')

        decision = input(str('Please enter a numbered option: '))

        if decision == '1':
            search = True
            
            while search:
                search = malAPICheck(user) # Returns True or False. False if done searching, true if continue to search

        elif decision == '2':
            viewWatchedList(user)

        elif decision == '3':
            commentOnSomeonesPage(user)

        elif decision == '4':
            viewComments(user)

        elif decision == '5':
            pass

        else: # log out
            logicGate = False
    
    print(f'Thank you! Goodbye')
    return