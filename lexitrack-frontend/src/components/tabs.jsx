// src/components/ui/tabs.jsx
import * as React from "react";
import * as TabsPrimitive from "@radix-ui/react-tabs";
import { cn } from "@/lib/utils"; // fonction pour combiner les classes tailwind (facultatif)

// Root Tabs
export const Tabs = ({ className, ...props }) => (
  <TabsPrimitive.Root className={cn("flex flex-col", className)} {...props} />
);
Tabs.displayName = "Tabs";

// Tabs List
export const TabsList = React.forwardRef(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex border-b border-muted-foreground bg-background/50 rounded-md p-1",
      className
    )}
    {...props}
  />
));
TabsList.displayName = "TabsList";

// Tabs Trigger (les onglets)
export const TabsTrigger = React.forwardRef(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center px-3 py-1 text-sm font-medium rounded-md text-muted-foreground hover:bg-muted/20 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground",
      className
    )}
    {...props}
  />
));
TabsTrigger.displayName = "TabsTrigger";

// Tabs Content
export const TabsContent = React.forwardRef(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn("mt-2 focus:outline-none", className)}
    {...props}
  />
));
TabsContent.displayName = "TabsContent";
