"""
Seed script for EduEnroll.

Populates the database with the 10 required courses (each with its modules
and topics) and creates a couple of demo student accounts so the app is
immediately usable after a fresh migrate.

Run with:
    python manage.py shell < seed.py
or:
    python seed.py   (after DJANGO_SETTINGS_MODULE is set, see bottom of file)
"""

import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduenroll.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Student, Course, Module, Topic

# Set to an int for reproducible seeding, or None to get a different
# random topic selection every time this script is run against a fresh DB.
RANDOM_SEED = None


COURSE_CATALOG = [
    {
        "name": "Java",
        "description": "Core language fundamentals through modern concurrent and functional Java.",
        "instructor": "R. Menon",
        "duration_weeks": 8,
        "modules": [
            ("Module 1: Core Java", ["Syntax & data types", "Operators & control flow", "Arrays & strings", "Type casting", "JVM basics"]),
            ("Module 2: OOPs", ["Classes & objects", "Inheritance", "Polymorphism", "Encapsulation & abstraction", "Interfaces vs abstract classes"]),
            ("Module 3: Collections", ["List, Set, Map", "Iterators", "Comparable & Comparator", "Queue & Deque", "Concurrent collections"]),
            ("Module 4: Multithreading", ["Thread lifecycle", "Synchronization", "Executor framework", "Locks & semaphores", "Thread pools"]),
            ("Module 5: Exception Handling", ["Try/catch/finally", "Checked vs unchecked", "Custom exceptions", "Try-with-resources", "Exception chaining"]),
            ("Module 6: Streams", ["Stream pipeline", "Lambdas", "Collectors", "Parallel streams", "Optional"]),
        ],
    },
    {
        "name": "Python",
        "description": "From syntax basics to packaging real, reusable Python modules.",
        "instructor": "A. Fernandes",
        "duration_weeks": 6,
        "modules": [
            ("Module 1: Basics", ["Variables & syntax", "Control flow", "Loops", "Input/output", "Comments & style"]),
            ("Module 2: Data Types", ["Numbers & strings", "Lists & tuples", "Dictionaries & sets", "Type conversion", "Mutability"]),
            ("Module 3: Functions", ["Defining functions", "Args & kwargs", "Closures & decorators", "Recursion", "Lambda functions"]),
            ("Module 4: OOPs", ["Classes & objects", "Inheritance", "Dunder methods", "Class vs instance attributes", "Multiple inheritance"]),
            ("Module 5: File Handling", ["Reading & writing files", "Context managers", "Working with CSV/JSON", "Binary files", "Exception-safe I/O"]),
            ("Module 6: Modules & Packages", ["Imports", "Creating packages", "Virtual environments", "pip & requirements", "__init__.py"]),
        ],
    },
    {
        "name": "DBMS",
        "description": "Relational database design, querying, and transaction fundamentals.",
        "instructor": "S. Iyer",
        "duration_weeks": 6,
        "modules": [
            ("Module 1: ER Diagrams", ["Entities & attributes", "Relationships", "Cardinality", "Weak entities", "ER to relational mapping"]),
            ("Module 2: Normalization", ["1NF & 2NF", "3NF & BCNF", "Denormalization trade-offs", "Functional dependencies", "Multi-valued dependencies"]),
            ("Module 3: SQL Queries", ["SELECT & filtering", "Joins", "Aggregation & GROUP BY", "Subqueries", "Window functions"]),
            ("Module 4: Transactions", ["ACID properties", "Isolation levels", "Locking", "Deadlocks", "Two-phase commit"]),
            ("Module 5: Indexing", ["B-tree indexes", "Composite indexes", "Query planning", "Covering indexes", "Index maintenance cost"]),
            ("Module 6: NoSQL Basics", ["Document stores", "Key-value stores", "CAP trade-offs", "Wide-column stores", "Eventual consistency"]),
        ],
    },
    {
        "name": "Data Structures & Algorithms (DSA)",
        "description": "Core data structures and the algorithmic thinking to use them well.",
        "instructor": "K. Rao",
        "duration_weeks": 10,
        "modules": [
            ("Module 1: Arrays", ["Array basics", "Two-pointer technique", "Sliding window", "Prefix sums", "In-place operations"]),
            ("Module 2: Linked Lists", ["Singly linked lists", "Doubly linked lists", "Cycle detection", "Reversal techniques", "Merge operations"]),
            ("Module 3: Stacks/Queues", ["Stack operations", "Queue & deque", "Monotonic stacks", "Circular queues", "Priority queues"]),
            ("Module 4: Trees", ["Binary trees", "BSTs", "Tree traversals", "Balanced trees", "Tries"]),
            ("Module 5: Sorting", ["Merge sort", "Quick sort", "Heap sort", "Counting sort", "Sorting stability"]),
            ("Module 6: Graph Algorithms", ["BFS & DFS", "Dijkstra's algorithm", "Union-Find", "Topological sort", "Minimum spanning trees"]),
        ],
    },
    {
        "name": "System Design",
        "description": "Design large-scale systems: from load balancers to message queues.",
        "instructor": "N. Kapoor",
        "duration_weeks": 8,
        "modules": [
            ("Module 1: Load Balancing", ["L4 vs L7 balancing", "Balancing algorithms", "Health checks", "Sticky sessions", "Failover strategies"]),
            ("Module 2: Caching", ["Cache-aside", "Write-through/back", "Eviction policies", "Cache invalidation", "Distributed caches"]),
            ("Module 3: Microservices", ["Service boundaries", "API gateways", "Service discovery", "Inter-service communication", "Circuit breakers"]),
            ("Module 4: Database Sharding", ["Horizontal vs vertical", "Shard keys", "Rebalancing", "Cross-shard queries", "Replication vs sharding"]),
            ("Module 5: CAP Theorem", ["Consistency", "Availability", "Partition tolerance trade-offs", "PACELC extension", "Real-world CAP choices"]),
            ("Module 6: Message Queues", ["Pub/sub vs point-to-point", "Delivery guarantees", "Backpressure", "Dead letter queues", "Ordering guarantees"]),
        ],
    },
    {
        "name": "Spring Boot",
        "description": "Build production-grade REST services on the Spring ecosystem.",
        "instructor": "R. Menon",
        "duration_weeks": 7,
        "modules": [
            ("Module 1: IoC", ["Beans & the container", "Dependency injection", "Bean scopes", "Auto-configuration", "Bean lifecycle"]),
            ("Module 2: MVC", ["Controllers", "Request mapping", "View resolution", "Model binding", "Validation"]),
            ("Module 3: Rest APIs", ["REST principles", "Building endpoints", "Exception handling", "DTOs & serialization", "Versioning"]),
            ("Module 4: Security", ["Authentication", "Authorization", "JWT basics", "CSRF protection", "Role-based access"]),
            ("Module 5: JPA/Hibernate", ["Entities & repositories", "Relationships", "Query methods", "Lazy vs eager loading", "Transactions in JPA"]),
            ("Module 6: Actuator", ["Health endpoints", "Metrics", "Custom endpoints", "Info endpoint", "Monitoring integration"]),
        ],
    },
    {
        "name": "NumPy",
        "description": "Fast numerical computing in Python with array-based programming.",
        "instructor": "A. Fernandes",
        "duration_weeks": 4,
        "modules": [
            ("Module 1: Arrays", ["Creating arrays", "Shapes & dtypes", "Array vs list", "Memory layout", "Views vs copies"]),
            ("Module 2: Indexing", ["Slicing", "Boolean indexing", "Fancy indexing", "Multi-dimensional indexing", "np.where"]),
            ("Module 3: Operations", ["Vectorized math", "Aggregations", "Reshaping", "Universal functions", "Sorting arrays"]),
            ("Module 4: Broadcasting", ["Broadcasting rules", "Common pitfalls", "Shape alignment", "Performance implications"]),
            ("Module 5: Linear Algebra", ["Matrix multiplication", "Determinants & inverses", "Eigenvalues", "Solving linear systems"]),
            ("Module 6: Random", ["Random generators", "Distributions", "Seeding", "Random sampling", "Shuffling arrays"]),
        ],
    },
    {
        "name": "Pandas",
        "description": "Wrangle, clean, and reshape tabular data for analysis.",
        "instructor": "P. Sharma",
        "duration_weeks": 4,
        "modules": [
            ("Module 1: Series", ["Creating a Series", "Indexing & alignment", "Vectorized operations", "Handling NaNs in a Series"]),
            ("Module 2: DataFrame", ["Creating a DataFrame", "Selecting rows/columns", "Filtering", "loc vs iloc", "Adding & dropping columns"]),
            ("Module 3: Data Cleaning", ["Handling missing data", "Type conversion", "Duplicates", "String cleaning", "Outlier handling"]),
            ("Module 4: Grouping", ["groupby basics", "Aggregations", "Transform & apply", "Multi-column grouping", "Custom agg functions"]),
            ("Module 5: Merging", ["Concat", "Merge & join", "Handling keys", "Join types", "Resolving overlapping columns"]),
            ("Module 6: Pivot Tables", ["pivot_table", "Cross-tabulation", "Reshaping with melt", "Stack & unstack", "Multi-index pivots"]),
        ],
    },
    {
        "name": "Machine Learning (ML)",
        "description": "Classical ML: regression, classification, clustering, and evaluation.",
        "instructor": "P. Sharma",
        "duration_weeks": 9,
        "modules": [
            ("Module 1: Regression", ["Linear regression", "Regularization", "Polynomial regression", "Gradient descent for regression", "Residual analysis"]),
            ("Module 2: Classification", ["Logistic regression", "k-NN", "Naive Bayes", "Decision boundaries", "Multi-class strategies"]),
            ("Module 3: Clustering", ["k-Means", "Hierarchical clustering", "DBSCAN", "Choosing k", "Cluster evaluation metrics"]),
            ("Module 4: SVM", ["Margins & kernels", "Soft margin", "Multi-class SVM", "Kernel trick", "Hyperparameter tuning"]),
            ("Module 5: Decision Trees", ["Splitting criteria", "Pruning", "Random forests", "Feature importance", "Overfitting in trees"]),
            ("Module 6: Model Evaluation", ["Train/test split", "Cross-validation", "Precision, recall, ROC", "Confusion matrix", "Bias-variance trade-off"]),
        ],
    },
    {
        "name": "Deep Learning (DL)",
        "description": "Neural network architectures from feed-forward nets to transformers.",
        "instructor": "V. Nair",
        "duration_weeks": 10,
        "modules": [
            ("Module 1: Neural Networks", ["Perceptrons", "Activation functions", "Forward pass", "Weight initialization", "Universal approximation"]),
            ("Module 2: Backpropagation", ["Chain rule", "Gradient descent", "Loss functions", "Learning rate scheduling", "Optimizers (SGD, Adam)"]),
            ("Module 3: CNN", ["Convolutions", "Pooling", "Classic architectures", "Feature maps", "Data augmentation"]),
            ("Module 4: RNN", ["Sequence modeling", "Vanishing gradients", "GRUs", "Backprop through time", "Bidirectional RNNs"]),
            ("Module 5: LSTMs", ["Gates & memory cells", "Sequence-to-sequence", "Attention with LSTMs", "Stacked LSTMs"]),
            ("Module 6: Transformers", ["Self-attention", "Positional encoding", "Encoder-decoder", "Multi-head attention", "Pretraining objectives"]),
        ],
    },
]


def seed_courses():
    """
    Creates the 10 courses with their modules. Each module's topic list is
    drawn as a random sample from a larger candidate pool, so the exact set
    of topics under a module varies between fresh seed runs while staying
    relevant to that module.
    """
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    created, skipped = 0, 0
    for entry in COURSE_CATALOG:
        course, was_created = Course.objects.get_or_create(
            name=entry["name"],
            defaults={
                "description": entry["description"],
                "instructor": entry["instructor"],
                "duration_weeks": entry["duration_weeks"],
            },
        )
        if not was_created:
            skipped += 1
            continue
        created += 1
        for i, (title, topic_pool) in enumerate(entry["modules"], start=1):
            module = Module.objects.create(course=course, module_number=i, title=title)
            # Randomly pick 3 topics (or fewer if the pool is smaller) from the pool.
            sample_size = min(3, len(topic_pool))
            chosen_topics = random.sample(topic_pool, sample_size)
            for topic_name in chosen_topics:
                Topic.objects.create(module=module, topic_name=topic_name)
    print(f"Courses created: {created}, already existed (skipped): {skipped}")


def seed_students():
    demo_users = [
        ("student1", "Aarav Shah", "aarav.shah@example.com", "eduenroll123"),
        ("student2", "Priya Nair", "priya.nair@example.com", "eduenroll123"),
    ]
    for username, name, email, password in demo_users:
        user, was_created = User.objects.get_or_create(
            username=username, defaults={"email": email}
        )
        if was_created:
            user.set_password(password)
            user.save()
        Student.objects.get_or_create(
            user=user, defaults={"name": name, "email": email}
        )
    print("Demo students ready: student1 / eduenroll123, student2 / eduenroll123")


def run():
    seed_courses()
    seed_students()


if __name__ == "__main__":
    run()
