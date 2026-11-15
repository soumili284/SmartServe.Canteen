import subprocess
import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SmartServe - Comprehensive Viva and Oral Examination Guide</title>
<style>
  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #2b1810;
    line-height: 1.55;
    font-size: 10.5pt;
    background: #ffffff;
  }
  h1 {
    color: #b45309;
    font-size: 20pt;
    border-bottom: 2px solid #f59e0b;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 12px;
  }
  h2 {
    color: #92400e;
    font-size: 14pt;
    border-bottom: 1px solid #fde68a;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }
  h3 {
    color: #78350f;
    font-size: 11.5pt;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }
  blockquote {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    margin: 8px 0;
    padding: 8px 14px;
    font-style: italic;
    color: #451a03;
    border-radius: 4px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }
  th {
    background: #fef3c7;
    color: #78350f;
    font-weight: bold;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #fde68a;
  }
  td {
    padding: 8px 10px;
    border: 1px solid #fde68a;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background: #fffdfa;
  }
  code {
    background: #fef3c7;
    color: #92400e;
    padding: 2px 5px;
    border-radius: 4px;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 9pt;
  }
  ul, ol {
    margin-top: 6px;
    margin-bottom: 10px;
    padding-left: 20px;
  }
  li {
    margin-bottom: 4px;
  }
  .tag {
    display: inline-block;
    background: #fef3c7;
    color: #b45309;
    border: 1px solid #fde68a;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 8.5pt;
    font-weight: bold;
  }
  .highlight-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 10px 0;
    page-break-inside: avoid;
  }
  .qa-block {
    margin-bottom: 12px;
    page-break-inside: avoid;
  }
  .qa-q {
    font-weight: bold;
    color: #9a3412;
  }
  .qa-a {
    margin-top: 4px;
    padding-left: 10px;
    border-left: 2px solid #fdba74;
  }
</style>
</head>
<body>

<h1>🎓 SmartServe: Comprehensive Viva & Oral Examination Guide</h1>
<span class="tag">C++ Object-Oriented Programming (OOPs)</span> &nbsp;
<span class="tag">Campus Digital Canteen & Token Queue System</span>

<h2>1. The 30-Second Elevator Pitch</h2>
<blockquote>
"SmartServe is a C++ Object-Oriented Canteen Management and Digital Token System designed to eliminate cafeteria congestion, long queues, and manual billing errors. It allows students and faculty to browse categorized menus with dietary filters, customize food orders, apply privilege discounts and coupons, and receive a sequential token number with an estimated wait time. Orders are tracked in real-time across kitchen queue states and backed by persistent file storage and a live localhost web dashboard."
</blockquote>

<h2>2. Real-World Problem vs. Solution</h2>
<table>
  <tr>
    <th style="width:45%;">The Problem (Manual Canteen)</th>
    <th style="width:55%;">SmartServe Solution</th>
  </tr>
  <tr>
    <td>Long counter queues during short recess/lunch breaks.</td>
    <td>Instant digital ordering with sequential token numbers (<code>TK-101</code>, <code>TK-102</code>).</td>
  </tr>
  <tr>
    <td>Confusion in the kitchen on what to cook first.</td>
    <td>Real-time queue board segregating orders into <b>Placed &rarr; Cooking &rarr; Ready for Pickup &rarr; Completed</b>.</td>
  </tr>
  <tr>
    <td>Manual calculation mistakes & lost paper slips.</td>
    <td>Automated itemized tax invoice calculation with GST and auto-saved receipt text files.</td>
  </tr>
  <tr>
    <td>Over-ordering items that are already out of stock.</td>
    <td>Real-time stock decrement and validation throwing <code>OutOfStockException</code>.</td>
  </tr>
</table>

<h2>3. The 4 Pillars of OOP (Examiner's Favorite Section)</h2>

<div class="highlight-box">
<h3>A. Encapsulation (Data Hiding & Validation)</h3>
<ul>
  <li><b>Definition</b>: Bundling data with methods operating on that data while restricting direct external access to object internals.</li>
  <li><b>In SmartServe</b>: All sensitive member variables (<code>price</code>, <code>stockQuantity</code>, <code>walletBalance</code>, <code>items</code>, <code>orderStatus</code>) are declared <code>private</code> or <code>protected</code>.</li>
  <li>External access is strictly controlled via validated getters and setters.</li>
  <li><b>Code Example</b>: In <code>MenuItem</code>, <code>reduceStock(int quantity)</code> verifies if <code>quantity &gt; stockQuantity</code> before reducing stock, throwing <code>OutOfStockException</code> if violated.</li>
</ul>
</div>

<div class="highlight-box">
<h3>B. Abstraction (Hiding Complexity)</h3>
<ul>
  <li><b>Definition</b>: Exposing only essential interfaces while concealing internal mechanics.</li>
  <li><b>In SmartServe</b>: Abstract base classes (<code>MenuItem</code>, <code>User</code>, <code>Payment</code>) define pure virtual methods (<code>= 0</code>) establishing what derived classes must implement without enforcing how.</li>
  <li>Complex algorithms (dynamic wait time estimation, ANSI terminal styling, file serialization) are cleanly hidden inside service classes like <code>TokenManager</code>, <code>FileStorage</code>, and <code>UIHelper</code>.</li>
</ul>
</div>

<div class="highlight-box">
<h3>C. Inheritance (Code Reusability & Extensibility)</h3>
<ul>
  <li><b>Definition</b>: Creating derived classes from existing base classes to model "is-a" relationships and share core logic.</li>
  <li><b>1. MenuItem Hierarchy</b>: Base <code>MenuItem</code> &rarr; <code>FoodItem</code> (dietary tag, spice level, prep time), <code>BeverageItem</code> (hot/cold, volume ml, caffeine), <code>ComboMeal</code> (bundled items, package savings).</li>
  <li><b>2. User Hierarchy</b>: Base <code>User</code> &rarr; <code>Student</code> (roll number, semester, 5% privilege discount), <code>Faculty</code> (employee ID, department, 10% discount), <code>Admin</code> (manager passcode, inventory management).</li>
  <li><b>3. Payment Hierarchy</b>: Base <code>Payment</code> &rarr; <code>CashPayment</code>, <code>UPIPayment</code>, <code>WalletPayment</code>, <code>CardPayment</code>.</li>
</ul>
</div>

<div class="highlight-box">
<h3>D. Polymorphism (One Interface, Multiple Behaviors)</h3>
<ul>
  <li><b>1. Runtime Polymorphism (Dynamic Binding / Overriding)</b>:
    <ul>
      <li>Achieved using virtual functions, pure virtual functions, and base class pointers/references (<code>std::shared_ptr&lt;MenuItem&gt;</code>, <code>std::shared_ptr&lt;User&gt;</code>).</li>
      <li>Calling <code>item-&gt;displayCard()</code> dynamically executes <code>FoodItem::displayCard()</code> or <code>BeverageItem::displayCard()</code> at runtime via the vtable.</li>
      <li>In payments, <code>payment-&gt;processPayment(amount)</code> polymorphically executes the selected strategy (UPI QR vs. cash change vs. wallet debit).</li>
    </ul>
  </li>
  <li><b>2. Compile-Time Polymorphism (Static Binding / Overloading)</b>:
    <ul>
      <li><b>Operator Overloading</b>: <code>operator&lt;&lt;</code> overloaded for <code>MenuItem</code> and <code>Order</code> to stream receipts cleanly into <code>std::cout</code> or files; <code>operator==</code> for item comparison.</li>
      <li><b>Function Overloading</b>: <code>getItemById(int)</code> vs <code>searchByName(string)</code>.</li>
    </ul>
  </li>
</ul>
</div>

<h2>4. System Architecture & Flow</h2>
<div class="highlight-box" style="font-family: monospace; font-size: 8.5pt;">
  [User Entry: Student / Faculty / Admin]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Browse Menu & Filter: Veg, Non-Veg, Category]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Add Items & Quantities to Cart (OrderItem)]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Apply Promo Coupon (CAMPUS50, WELCOME10) & Role Discount]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Select Payment Strategy (Cash / UPI / Wallet / Card)]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Validate Stock & Deduct Inventory]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Generate Token Number (e.g. TK-101) & Estimated Time]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Save Tax Invoice Receipt (.txt) & Append to History Log]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Order enters Live Queue (TokenManager)]<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&darr;<br>
  [Kitchen Staff Advances: Placed &rarr; Cooking &rarr; Ready &rarr; Completed]
</div>

<h2>5. Top 15 Frequently Asked Viva Questions & Answers</h2>

<div class="qa-block">
  <div class="qa-q">Q1: Why did you use virtual destructors in your base classes?</div>
  <div class="qa-a"><b>Answer:</b> When deleting a derived object through a base pointer (<code>MenuItem*</code> or <code>std::shared_ptr&lt;MenuItem&gt;</code>), a non-virtual destructor only invokes the base destructor, causing undefined behavior and <b>memory leaks</b>. A virtual destructor guarantees the derived destructor executes first, properly releasing all derived resources.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q2: Why did you use std::shared_ptr instead of raw pointers (new / delete)?</div>
  <div class="qa-a"><b>Answer:</b> <code>std::shared_ptr</code> provides automatic reference counting and RAII (Resource Acquisition Is Initialization). It prevents memory leaks, dangling pointers, and double-free bugs by releasing memory automatically when all references go out of scope.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q3: What design pattern is used in your payment system?</div>
  <div class="qa-a"><b>Answer:</b> The <b>Strategy Design Pattern</b>. The <code>Payment</code> abstract base class defines the algorithm interface <code>processPayment(double amount)</code>, and concrete classes (<code>CashPayment</code>, <code>UPIPayment</code>, <code>WalletPayment</code>, <code>CardPayment</code>) encapsulate specific behaviors. The <code>Order</code> context interacts solely with the abstract strategy.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q4: How is dynamic wait time calculated?</div>
  <div class="qa-a"><b>Answer:</b> In <code>Order::calculateBill()</code>: <code>Estimated Minutes = 5 + (Total Items &times; 2)</code> (capped between 5 and 35 minutes for realism).</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q5: How are tokens generated and tracked?</div>
  <div class="qa-a"><b>Answer:</b> <code>TokenManager</code> maintains an atomic counter starting at 101. Active orders are stored in <code>std::map&lt;int, std::shared_ptr&lt;Order&gt;&gt;</code>. When finished, they move to completed order history.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q6: What happens if an item runs out of stock while placing an order?</div>
  <div class="qa-a"><b>Answer:</b> <code>MenuItem::reduceStock()</code> validates available stock and throws an <code>OutOfStockException</code> if insufficient. The main controller catches this, displays an error message, and protects inventory integrity.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q7: What is the difference between compile-time and runtime polymorphism in your code?</div>
  <div class="qa-a"><b>Answer:</b>
    <ul>
      <li><b>Compile-time (Static)</b>: Resolved at compile time via function overloading and operator overloading (e.g., <code>operator&lt;&lt;</code>).</li>
      <li><b>Runtime (Dynamic)</b>: Resolved at runtime via virtual functions and vtables when calling methods through base pointers (e.g., <code>item-&gt;displayCard()</code>).</li>
    </ul>
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">Q8: How does the data persistence work?</div>
  <div class="qa-a"><b>Answer:</b> Delimited text files are used: <code>data/menu.txt</code> for menu records, <code>data/orders_history.txt</code> for order audit logs, and <code>receipts/receipt_TK*.txt</code> for printable customer invoices.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q9: What are the role privileges and how do they work?</div>
  <div class="qa-a"><b>Answer:</b> The base class <code>User</code> specifies pure virtual <code>getDiscountRate()</code>. <code>Student</code> returns 0.05 (5%), <code>Faculty</code> returns 0.10 (10%), and <code>Admin</code> has management privileges.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q10: How does the promo coupon system work?</div>
  <div class="qa-a"><b>Answer:</b>
    <ul>
      <li><code>CAMPUS50</code>: Flat &#8377;50 off for cart value &ge; &#8377;200.</li>
      <li><code>WELCOME10</code>: 10% discount on cart value.</li>
      <li><code>SNACK5</code>: Flat &#8377;5 off for cart value &ge; &#8377;50.</li>
    </ul>
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">Q11: How does the web interface connect to the C++ system?</div>
  <div class="qa-a"><b>Answer:</b> A Python multi-threaded HTTP server (<code>server.py</code>) serves an interactive web application (<code>public/index.html</code>) on <code>http://localhost:5000</code>, reading and writing to the identical C++ data files (<code>data/menu.txt</code>, <code>data/orders_history.txt</code>, and <code>receipts/</code>).</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q12: Why did you use custom exceptions?</div>
  <div class="qa-a"><b>Answer:</b> Inheriting from <code>std::runtime_error</code> allows clean exception discrimination (e.g. <code>OutOfStockException</code> vs <code>PaymentFailedException</code>) and descriptive context messages.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q13: What is the role of UIHelper?</div>
  <div class="qa-a"><b>Answer:</b> It centralizes ANSI colored terminal styling and provides crash-proof input functions (<code>getIntInput</code>, <code>getDoubleInput</code>) preventing infinite buffer loops on invalid input.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q14: How does kitchen staff manage orders?</div>
  <div class="qa-a"><b>Answer:</b> Kitchen staff authenticate with passcode <code>admin123</code>. They advance orders through states: <b>Placed &rarr; In Kitchen / Cooking &rarr; Ready for Pickup &rarr; Completed</b>, updating the live queue instantly.</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q15: What are future enhancements you would add?</div>
  <div class="qa-a"><b>Answer:</b> Database persistence (SQLite/PostgreSQL), SMS/WhatsApp notifications on order readiness, and barcode/QR verification at pickup.</div>
</div>

<h2>6. Quick Pre-Viva Checklist</h2>
<div class="highlight-box">
<ol>
  <li><b>Starting Token Number</b>: <code>101</code></li>
  <li><b>Admin Password</b>: <code>admin123</code></li>
  <li><b>Privilege Discounts</b>: Student = <b>5%</b>, Faculty = <b>10%</b>, Tax = <b>5% GST</b></li>
  <li><b>Promo Coupons</b>: <code>CAMPUS50</code>, <code>WELCOME10</code>, <code>SNACK5</code></li>
  <li><b>Executables & Run Scripts</b>:
    <ul>
      <li>C++ Console Program: <code>bin/SmartServe.exe</code> (run via <code>.\\run.bat</code>)</li>
      <li>Localhost Web Dashboard: <code>server.py</code> on <code>http://localhost:5000</code> (run via <code>.\\run_web.bat</code>)</li>
    </ul>
  </li>
</ol>
</div>

</body>
</html>
"""

with open("viva_guide.html", "w", encoding="utf-8") as f:
    f.write(html_content)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

html_path = os.path.abspath("viva_guide.html")
pdf_path = os.path.abspath("SmartServe_Viva_Preparation_Guide.pdf")

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path.replace(os.sep, '/')}"
]

print("Executing PDF generation...")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path):
    print("SUCCESS! PDF created at:", pdf_path, "Size:", os.path.getsize(pdf_path), "bytes")
else:
    print("Failed to create PDF. Stderr:", res.stderr)
