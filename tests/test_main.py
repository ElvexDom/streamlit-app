from app.main import main


# Test de la fonction main directement
def test_front_main_output(capsys):
    """Vérifie que la fonction main affiche le bon message dans la console."""
    main()
    captured = capsys.readouterr()
    assert "Hello from streamlit-app!" in captured.out
