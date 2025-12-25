#!/bin/bash
# Deployment verification script for Lemons Family Cookbook
# Run after each deploy to verify all routes work

BASE="${1:-https://joelev.github.io/lemons-family-cookbook}"
FAILED=0

echo "=== DEPLOYMENT VERIFICATION ==="
echo "Base URL: $BASE"
echo ""

check_url() {
  local path="$1"
  local desc="$2"
  local status=$(curl -sI "${BASE}${path}" | grep "HTTP" | head -1 | awk '{print $2}')
  if [ "$status" = "200" ]; then
    echo "✓ $desc"
  else
    echo "✗ $desc (HTTP $status)"
    FAILED=$((FAILED + 1))
  fi
}

echo "=== Core Pages ==="
check_url "/" "Homepage"
check_url "/recipes/" "All Recipes"

echo ""
echo "=== Category Pages ==="
check_url "/category/cakes-pies-frostings/" "Cakes & Pies"
check_url "/category/candies-cookies-confections/" "Cookies & Candy"
check_url "/category/main-dishes-meats-vegetables/" "Main Dishes"
check_url "/category/quickbreads-muffins-pancakes/" "Quick Breads"
check_url "/category/salads/" "Salads"
check_url "/category/yeast-breads-rolls-sweet-dough/" "Yeast Breads"

echo ""
echo "=== Sample Recipe Pages ==="
check_url "/recipe/german_chocolate_cake/" "German Chocolate Cake"
check_url "/recipe/grandma_lemons_sugar_cookies/" "Grandma's Sugar Cookies"
check_url "/recipe/home_made_bread/" "Home Made Bread"
check_url "/recipe/potato_salad/" "Potato Salad"
check_url "/recipe/my_pancakes_or_waffles/" "Pancakes or Waffles"

echo ""
echo "=== Redirect Behavior ==="
redirect_status=$(curl -sI "${BASE}/category/salads" | grep "HTTP" | head -1 | awk '{print $2}')
if [ "$redirect_status" = "301" ]; then
  echo "✓ No-trailing-slash redirects correctly (301)"
else
  echo "✗ No-trailing-slash should 301, got $redirect_status"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "=== Link Validation ==="
# Check that internal links have correct base path
bad_links=$(curl -s "${BASE}/" | grep -oE 'href="/[^l][^"]*"' | grep -v "lemons-family-cookbook" | head -3)
if [ -z "$bad_links" ]; then
  echo "✓ All internal links include base path"
else
  echo "✗ Found links missing base path:"
  echo "$bad_links"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "================================"
if [ $FAILED -eq 0 ]; then
  echo "All checks passed!"
  exit 0
else
  echo "$FAILED check(s) failed"
  exit 1
fi
