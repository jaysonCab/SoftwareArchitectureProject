def checkBadgesForUser(user, animeTitle, db):
    '''
    Only programmed for two types of badges. If the title of one show is one piece or
    the user has at least 10 shows logged in their watched shows. Easily countable by length function.
    Is scalable, just add more checks here.
    '''
    
    watchedCount = len(user.watched_shows)

    # Badge 101 = One Piece Fanatic
    if animeTitle.lower() == "one piece":
        tryAward(user.id, 101, db)

    # Badge 102 = 10 Shows Watched
    if watchedCount >= 10:
        tryAward(user.id, 102, db)

def tryAward(user_id, badge_number, db):
    '''
    userHasBadge returns true or false, if doesn't exist then award a badge
    '''

    if not userHasBadge(user_id, badge_number, db):
        awardBadge(user_id, badge_number, db)

def userHasBadge(user_id, badge_number, db):
    
    # Select 1 simply returns anything if it exists, the content doesn't matter
    db.cursor.execute("""
        SELECT 1
        FROM software_architecture_user_badges
        WHERE user_id = %s AND badge_number = %s
        LIMIT 1
    """, (user_id, badge_number))

    return db.cursor.fetchone() is not None

def awardBadge(user_id, badge_number, db):

    # Simple insert into table that holds user id and badge number mappings
    db.cursor.execute("""
        INSERT INTO software_architecture_user_badges (user_id, badge_number)
        VALUES (%s, %s)
    """, (user_id, badge_number))
    db.commit()

    print(f"You've earned a new badge! (#{badge_number})")