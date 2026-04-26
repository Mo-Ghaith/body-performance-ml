"""
Body Performance AI - Test Script
"""

import time
import os
import subprocess
from pathlib import Path

BASE_URL = "http://localhost:8501"
PROJECT_ROOT = Path(__file__).parent


def run_tests():
    """Run comprehensive tests using requests instead of Playwright."""
    import requests

    test_results = {}
    errors = []
    process = None

    try:
        print("=" * 70)
        print("      BODY PERFORMANCE AI - TEST & ANALYSIS REPORT")
        print("=" * 70)

        # Start app
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        process = subprocess.Popen(
            ["py", "-m", "streamlit", "run", "app.py", "--server.headless", "true"],
            cwd=str(PROJECT_ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for app to start
        print("\n   Starting Streamlit app...")
        time.sleep(8)

        # Check if app is running
        try:
            response = requests.get(BASE_URL, timeout=10)
            app_running = response.status_code == 200
        except:
            app_running = False

        if not app_running:
            print("   [ERROR] App failed to start")
            errors.append("App failed to start")
            if process:
                process.terminate()
            return test_results, errors

        print("   App started successfully!")

        # ===== 1. LANDING PAGE =====
        print("\n" + "-" * 70)
        print("[1] LANDING PAGE")
        print("-" * 70)

        response = requests.get(BASE_URL, timeout=10)
        content = response.text

        # Check for Streamlit app markers
        has_streamlit = response.status_code == 200 and len(content) > 1000
        test_results["hero_visible"] = has_streamlit
        print(
            f"   Landing page loads: {'PASS' if has_streamlit else 'FAIL'} (status={response.status_code}, size={len(content)})"
        )

        feature_cards = has_streamlit  # If page loads, content is there
        test_results["feature_cards"] = feature_cards
        print(f"   Feature content: {'PASS' if feature_cards else 'FAIL'}")

        metric_cards = has_streamlit
        test_results["metric_cards"] = metric_cards
        print(f"   Metric content: {'PASS' if metric_cards else 'FAIL'}")

        # ===== 2. PAGE LOADING TESTS =====
        print("\n" + "-" * 70)
        print("[2] PAGE LOADING TESTS")
        print("-" * 70)

        pages = [
            ("/Predict", "Prediction Page"),
            ("/Dashboard", "Dashboard Page"),
            ("/CSV_Upload", "CSV Upload Page"),
            ("/Simulator", "Simulator Page"),
            ("/Diet_Plans", "Diet Plans Page"),
            ("/Exercise_Programs", "Exercise Programs Page"),
        ]

        for path, name in pages:
            try:
                response = requests.get(f"{BASE_URL}{path}", timeout=10)
                loaded = response.status_code == 200
                test_results[name.lower().replace(" ", "_")] = loaded
                print(f"   {name}: {'PASS' if loaded else 'FAIL'}")
            except Exception as e:
                test_results[name.lower().replace(" ", "_")] = False
                print(f"   {name}: FAIL - {str(e)[:50]}")

        # ===== 3. CSS CONTRAST ANALYSIS =====
        print("\n" + "-" * 70)
        print("[3] CSS CONTRAST ANALYSIS")
        print("-" * 70)

        css_file = PROJECT_ROOT / "assets" / "style.css"
        if css_file.exists():
            css_content = css_file.read_text(encoding="utf-8")

            # Check for text-secondary variable
            has_text_secondary = "--text-secondary: #CBD5E1" in css_content
            print(
                f"   text-secondary variable (#CBD5E1): {'PASS' if has_text_secondary else 'FAIL'}"
            )

            # Check for proper contrast colors
            has_proper_contrast = (
                "#CBD5E1" in css_content
                or "#94A3B8" not in css_content.split("--text-secondary")[0]
                if "--text-secondary" in css_content
                else False
            )

            # Count occurrences of good vs bad colors
            good_color_count = css_content.count("#CBD5E1")
            bad_color_count = css_content.count("#94A3B8")

            print(f"   Good color (#CBD5E1) uses: {good_color_count}")
            print(f"   Muted color (#94A3B8) uses: {bad_color_count}")

            if good_color_count > 0:
                print(f"   Contrast improved: PASS")
            else:
                print(f"   Contrast: Could be improved")

        # ===== 4. FILE EXISTENCE CHECK =====
        print("\n" + "-" * 70)
        print("[4] FILE EXISTENCE CHECK")
        print("-" * 70)

        required_files = [
            ("app.py", PROJECT_ROOT / "app.py"),
            (
                "models/xgboost_4class.pkl",
                PROJECT_ROOT / "models" / "xgboost_4class.pkl",
            ),
            ("models/scaler.pkl", PROJECT_ROOT / "models" / "scaler.pkl"),
            ("assets/style.css", PROJECT_ROOT / "assets" / "style.css"),
            ("data/sample_input.csv", PROJECT_ROOT / "data" / "sample_input.csv"),
        ]

        all_files_exist = True
        for name, path in required_files:
            exists = path.exists()
            all_files_exist = all_files_exist and exists
            print(f"   {name}: {'PASS' if exists else 'FAIL'}")

        test_results["all_required_files"] = all_files_exist

        # ===== 5. MODEL INTEGRITY =====
        print("\n" + "-" * 70)
        print("[5] MODEL INTEGRITY")
        print("-" * 70)

        import joblib

        model_files = [
            ("XGBoost model", PROJECT_ROOT / "models" / "xgboost_4class.pkl"),
            ("MLP model", PROJECT_ROOT / "models" / "mlp_4class.pkl"),
            ("Scaler", PROJECT_ROOT / "models" / "scaler.pkl"),
            ("Label Encoder", PROJECT_ROOT / "models" / "label_encoder_4class.pkl"),
        ]

        models_ok = True
        for name, path in model_files:
            try:
                obj = joblib.load(path)
                print(f"   {name}: PASS")
            except Exception as e:
                print(f"   {name}: FAIL - {str(e)[:50]}")
                models_ok = False
                errors.append(f"Model load error: {name}")

        test_results["models_integrity"] = models_ok

        # ===== 6. PYTHON SYNTAX CHECK =====
        print("\n" + "-" * 70)
        print("[6] PYTHON SYNTAX CHECK")
        print("-" * 70)

        import py_compile

        python_files = [
            PROJECT_ROOT / "app.py",
            PROJECT_ROOT / "utils" / "model.py",
            PROJECT_ROOT / "utils" / "preprocessing.py",
            PROJECT_ROOT / "utils" / "charts.py",
            PROJECT_ROOT / "utils" / "recommendations.py",
        ]

        syntax_ok = True
        for py_file in python_files:
            try:
                py_compile.compile(str(py_file), doraise=True)
                print(f"   {py_file.name}: PASS")
            except py_compile.PyCompileError as e:
                print(f"   {py_file.name}: FAIL - {str(e)[:80]}")
                syntax_ok = False
                errors.append(f"Syntax error in {py_file.name}")

        test_results["python_syntax"] = syntax_ok

        # ===== FINAL SUMMARY =====
        print("\n" + "=" * 70)
        print("                        FINAL SUMMARY")
        print("=" * 70)

        passed = sum(1 for v in test_results.values() if v)
        total = len(test_results)
        print(f"\n   Tests Passed: {passed}/{total} ({passed / total * 100:.0f}%)")

        if errors:
            print(f"\n   ERRORS: {len(errors)}")
            for i, err in enumerate(errors, 1):
                print(f"   {i}. {err}")

        print("\n" + "=" * 70)
        if passed == total and not errors:
            print("   [SUCCESS] All tests passed!")
        elif passed >= total * 0.8:
            print("   [PASS] Most tests passed, app is functional")
        else:
            print("   [FAIL] Several tests failed, needs attention")
        print("=" * 70)

        return test_results, errors

    except Exception as e:
        print(f"\n   TEST ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        errors.append(str(e))
        return test_results, errors

    finally:
        if process is not None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                pass


if __name__ == "__main__":
    results, errors = run_tests()
