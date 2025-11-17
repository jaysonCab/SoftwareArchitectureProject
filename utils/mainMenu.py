from utils.mainAPI import malAPICheck
from utils.mainDatabase import Database

def viewWatchedList(user):
    '''
    Function used if the user wants to checkk their watched shows. Queries the users own watched_shows
    variable. If nothing, state nothing is located. If something exists, display all in a loop.
    '''
    
    print("\nYour watched shows:")

    if not user.watched_shows:
        print("You haven't added any shows yet.")

    else:
        for show in user.watched_shows:
            print(f"- {show.show_name} (Your rating: {show.personal_score})")

    input("Press Enter to go back to main menu...")

    return

def viewComments(user):
    '''
    Separate code places comments on a users profile, this one searches for the comments
    and displays for a given user.
    credentials table matches the user_id to the associated name to be displayed
    profile_comments table matches the user_id_commenter (joined with credentials table)
    to display the actual comment.
    '''
    
    db = Database()
    print("\nComments on your page:\n")

    db.cursor.execute("""
        select pc.comment, u.username
        from software_architecture_profile_comments pc
        join software_architecture_credentials u
            on pc.user_id_commenter = u.id
        where pc.user_id_profile = %s
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
    '''
    From main page you can place comments on other peoples pages.
    '''
    
    print("\nList of all users:")

    db = Database()
    db.cursor.execute(""" 
        select id, username 
        from software_architecture_credentials
        where id != %s
    """, (currentUser.id,))         # Get all users except the current user

    rows = db.cursor.fetchall()

    if not rows:
        print("No other users exist.")
        return

    # Display users in a numbered list
    for i, (user_id, username) in enumerate(rows, start=1):
        print(f"({i}) --> {username}")

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
        insert into software_architecture_profile_comments (user_id_profile, user_id_commenter, comment)
        values (%s, %s, %s)
        """, (selected_user_id, currentUser.id, comment_text)
    )

    db.commit()

    print("Comment posted successfully!")
    input("Press Enter to go back to main menu...")

    return

def viewBadges(user):
    '''
    Simple join statement. There is one table that holds all of the obtainable badges, and a second table
    that matches badge number aquired to users. By joining, you get both the user and the description of
    the badge unlocked.
    '''
    
    db = Database()
    print("\nYour Badges:")

    db.cursor.execute("""
        select b.badge_name, b.badge_description
        from software_architecture_user_badges ub
        join software_architecture_badges b
            on ub.badge_number = b.badge_number
        where ub.user_id = %s
    """, (user.id,))

    rows = db.cursor.fetchall()

    if not rows:
        print("You have no badges yet.")
        input("Press Enter to go back...")
        return

    for badge_name, badge_description in rows:
        print(f"- {badge_name}: {badge_description}")

    input("Press Enter to go back...")

def mainMenu(user):
    '''
    Main menu decision tree on what you are capable of doing.
    In a while loop until they decide to log out.
    '''
    
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
            viewBadges(user)

        else: # log out
            logicGate = False
    
    print(f'Thank you! Goodbye')
    return