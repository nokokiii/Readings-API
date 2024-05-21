from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from repositories import AuthorRepository, EpochRepository, GenreRepository, KindRepository, BookRepository
from db.scheme import Base  # Import your Base model for creating the database schema

# Blueprint for the book routes
book_bp = Blueprint('book', __name__)

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

@book_bp.route('/add_book', methods=['POST'])
def add_book():
    # Create a session
    session = create_session(book_bp.engine)
    
    try:
        # Get data from the request
        data = request.json
        title = data['title']
        author_name = data['author_name']
        epoch_name = data['epoch_name']
        genre_name = data['genre_name']
        kind_name = data['kind_name']
        
        # Initialize repositories
        author_repo = AuthorRepository(session)
        epoch_repo = EpochRepository(session)
        genre_repo = GenreRepository(session)
        kind_repo = KindRepository(session)
        book_repo = BookRepository(session)
        
        # Get or create category entries
        author = author_repo.get_or_create(author_name)
        epoch = epoch_repo.get_or_create(epoch_name)
        genre = genre_repo.get_or_create(genre_name)
        kind = kind_repo.get_or_create(kind_name)
        
        # Add the new book
        new_book = book_repo.add_book(title, author, epoch, genre, kind)
        
        # Commit the transaction
        session.commit()
        
        # Return the new book details as JSON
        return jsonify({
            'id': new_book.id,
            'title': new_book.title,
            'author': new_book.author.name,
            'epoch': new_book.epoch.name,
            'genre': new_book.genre.name,
            'kind': new_book.kind.name
        }), 201
    except Exception as e:
        # Rollback the transaction in case of an error
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Close the session
        session.close()
