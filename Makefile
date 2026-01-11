# Compiler settings
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2

# Target executable
TARGET = pdf_processor

# Source files
SOURCES = pdf_processor.cpp
OBJECTS = $(SOURCES:.cpp=.o)

# Default target
all: $(TARGET)

# Build the executable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)
	@echo "Build complete: $(TARGET)"

# Compile source files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Run demo
demo: $(TARGET)
	./$(TARGET)

# Clean build artifacts
clean:
	rm -f $(OBJECTS) $(TARGET)
	@echo "Clean complete"

# Help
help:
	@echo "Available targets:"
	@echo "  all   - Build the PDF processor (default)"
	@echo "  demo  - Build and run demo"
	@echo "  clean - Remove build artifacts"
	@echo "  help  - Show this help message"

.PHONY: all demo clean help
