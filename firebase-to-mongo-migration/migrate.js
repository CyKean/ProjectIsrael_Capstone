// const admin = require('firebase-admin');
// const { MongoClient } = require('mongodb');

// // 1. Initialize Firebase Admin SDK
// // IMPORTANT: Download your service account key from Firebase Console > Project Settings > Service Accounts
// const serviceAccount = require('./hindiItoApiKey.json');

// admin.initializeApp({
//   credential: admin.credential.cert(serviceAccount)
// });
// const firestore = admin.firestore();

// // 2. Initialize MongoDB Client
// // Replace with your MongoDB connection string (e.g., MongoDB Atlas URI or localhost)
// // const mongoUri = 'mongodb+srv://projectisraelcapstone:KpWXU4nC5EzCauID@cluster0.jvbrvzi.mongodb.net/projectisrael_db?retryWrites=true&w=majority&appName=Cluster0';
// const mongoUri = 'mongodb://127.0.0.1:27017/projectisrael_db';
// const client = new MongoClient(mongoUri);

// // 3. List ALL collections to be migrated
// // Add all your collection names to this array. The name is the same in Firebase and MongoDB.
// const collectionsToMigrate = [
//   'sensor_readings',
//   'app_metrics',
//   'configurations',
//   'crop_recommendations',
//   'metric_history',
//   'motor_status',
//   'network',
//   'notifications',
//   'password_reset_codes',
//   'system_stats',
//   'users',
//   'water_level_readings',
//   'watering_schedules',
//   'weather_data'
// ];

// // 4. Universal transformation function for a document
// function transformDocument(data) {
//   // Create a shallow copy of the data to avoid modifying the original
//   const transformedData = { ...data };

//   // Recursively traverse the document and transform specific fields
//   function traverse(obj) {
//     for (let key in obj) {
//       if (obj.hasOwnProperty(key)) {
//         const value = obj[key];

//         // Check if this is a Firestore Timestamp and convert to JS Date
//         if (value && typeof value === 'object' && 'toDate' in value && typeof value.toDate === 'function') {
//           obj[key] = value.toDate(); // Convert to native Date object
//         }
//         // Check if this is a Firestore DocumentReference and convert to path string
//         else if (value && typeof value === 'object' && 'path' in value) {
//           obj[key] = value.path; // Convert to its string path
//         }
//         // Check if this is a Firestore GeoPoint
//         else if (value && typeof value === 'object' && 'latitude' in value && 'longitude' in value) {
//           // Convert to a format MongoDB understands for geospatial queries
//           obj[key] = {
//             type: 'Point',
//             coordinates: [value.longitude, value.latitude] // MongoDB uses [long, lat]
//           };
//         }
//         // If it's a nested object or array, traverse it recursively
//         else if (value && typeof value === 'object' && !Array.isArray(value)) {
//           traverse(value);
//         }
//         // If it's an array, check each element
//         else if (Array.isArray(value)) {
//           value.forEach(item => {
//             if (item && typeof item === 'object') {
//               traverse(item);
//             }
//           });
//         }
//       }
//     }
//   }

//   traverse(transformedData);
//   return transformedData;
// }

// // 5. Main migration function for a single collection
// async function migrateCollection(collectionName) {
//   let mongoCollection = null;
//   console.log(`\nStarting migration for collection: ${collectionName}`);

//   try {
//     const firebaseCollection = firestore.collection(collectionName);
//     mongoCollection = client.db('projectisrael_db').collection(collectionName); // Use the same collection name

//     // Get all documents from the Firebase collection
//     const snapshot = await firebaseCollection.get();

//     if (snapshot.empty) {
//       console.log(`  -> Collection '${collectionName}' is empty. Skipping.`);
//       return { success: true, count: 0 };
//     }

//     console.log(`  -> Found ${snapshot.size} documents. Preparing for MongoDB...`);

//     const operations = [];
//     const batchSize = 500; // Process in batches to avoid memory overload
//     let processedCount = 0;

//     // Process each document
//     for (const doc of snapshot.docs) {
//       let firebaseData = doc.data();
      
//       // Apply the universal transformation
//       const mongoData = transformDocument(firebaseData);

//       // Prepare the operation for bulk write
//       operations.push({
//         insertOne: {
//           document: {
//             _id: doc.id, // Preserve the original Firestore document ID
//             ...mongoData
//           }
//         }
//       });

//       processedCount++;

//       // Execute in batches
//       if (operations.length >= batchSize) {
//         const result = await mongoCollection.bulkWrite(operations, { ordered: false });
//         console.log(`  -> Inserted batch of ${operations.length} into MongoDB.`);
//         operations.length = 0; // Clear the array for the next batch
//       }
//     }

//     // Insert any remaining documents in the final batch
//     if (operations.length > 0) {
//       const result = await mongoCollection.bulkWrite(operations, { ordered: false });
//       console.log(`  -> Inserted final batch of ${operations.length} into MongoDB.`);
//     }

//     console.log(`  ✅ SUCCESS: Migrated ${processedCount} documents from '${collectionName}'.`);
//     return { success: true, count: processedCount };

//   } catch (error) {
//     console.error(`  ❌ ERROR migrating collection '${collectionName}':`, error.message);
//     return { success: false, error: error.message, count: 0 };
//   }
// }

// // 6. Master function to run the entire migration
// async function runFullMigration() {
//   const migrationResults = {};

//   try {
//     await client.connect();
//     console.log('Connected to MongoDB successfully.');

//     // Migrate each collection sequentially
//     for (const collectionName of collectionsToMigrate) {
//       migrationResults[collectionName] = await migrateCollection(collectionName);
//       // Add a small delay between collections if needed to avoid overwhelming the database
//       // await new Promise(resolve => setTimeout(resolve, 100));
//     }

//     console.log('\n----- Migration Summary -----');
//     let totalDocs = 0;
//     for (const [collection, result] of Object.entries(migrationResults)) {
//       const status = result.success ? '✅' : '❌';
//       console.log(`${status} ${collection}: ${result.count} documents. ${result.error || ''}`);
//       totalDocs += result.count;
//     }
//     console.log(`\nTotal documents migrated: ${totalDocs}`);

//   } catch (error) {
//     console.error('A fatal error occurred:', error);
//   } finally {
//     await client.close();
//     console.log('MongoDB connection closed.');
//     process.exit(0); // Exit the script
//   }
// }

// // 7. Run the script
// runFullMigration();

const admin = require('firebase-admin');
const { MongoClient } = require('mongodb');

// Initialize Firebase Admin SDK
const serviceAccount = require('./hindiItoApiKey.json');
admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });
const firestore = admin.firestore();

// Initialize MongoDB Client
// const mongoUri = 'mongodb+srv://projectisraelcapstone:KpWXU4nC5EzCauID@cluster0.jvbrvzi.mongodb.net/projectisrael_db?retryWrites=true&w=majority&appName=Cluster0';
const mongoUri = 'mongodb://127.0.0.1:27017/projectisrael_db';
const client = new MongoClient(mongoUri);

// Migration configuration
const BATCH_SIZE = 100;

// Collection-specific migration handlers
const collectionHandlers = {
  // 1. sensor_readings: Embedded approach for device readings
  async 'sensor_readings'() {
    console.log('📊 Migrating sensor_readings...');
    const mongoCollection = client.db('projectisrael_db').collection('sensor_readings');
    const devicesCollection = firestore.collection('3sensor_readings');
    
    const devices = await devicesCollection.listDocuments();
    const operations = [];
    
    for (const deviceRef of devices) {
      const deviceId = deviceRef.id;
      const readingsRef = deviceRef.collection('readings');
      const readingsSnapshot = await readingsRef.get();
      
      if (!readingsSnapshot.empty) {
        const deviceData = {
          _id: deviceId,
          readings: readingsSnapshot.docs.map(doc => ({
            _id: doc.id,
            ...doc.data()
          }))
        };
        operations.push({ insertOne: { document: deviceData } });
        console.log(`  -> Device ${deviceId}: ${readingsSnapshot.size} readings`);
      }
    }
    
    if (operations.length > 0) {
      await mongoCollection.bulkWrite(operations, { ordered: false });
    }
    return operations.length;
  },

  // 2. motor_status: Complex nested structure
  async 'motor_status'() {
    console.log('📊 Migrating motor_status...');
    const mongoCollection = client.db('projectisrael_db').collection('motor_status');
    const motorStatusCollection = firestore.collection('motor_status');
    
    const operations = [];
    let docCount = 0;

    // Get all documents in motor_status collection
    const statusDocs = await motorStatusCollection.get();
    
    for (const doc of statusDocs.docs) {
        const docId = doc.id; // This will be "current" or "history"
        const docData = { _id: docId, ...doc.data() };
        
        console.log(`  -> Processing ${docId}...`);

        // Handle the "current" document structure
        if (docId === 'current') {
        // Check if "current" has a "history" subcollection
        try {
            const historySubcollection = doc.ref.collection('history');
            const historySnapshot = await historySubcollection.get();
            
            if (!historySnapshot.empty) {
            docData.history = historySnapshot.docs.map(historyDoc => ({
                _id: historyDoc.id,
                ...historyDoc.data()
            }));
            console.log(`    ↳ Found ${historySnapshot.size} history entries in current`);
            }
        } catch (error) {
            console.log(`    ↳ No history subcollection in current document`);
        }
        }
        
        // Handle the "history" document structure  
        if (docId === 'history') {
        // Check if "history" has a "logs" subcollection
        try {
            const logsSubcollection = doc.ref.collection('logs');
            const logsSnapshot = await logsSubcollection.get();
            
            if (!logsSnapshot.empty) {
            docData.logs = logsSnapshot.docs.map(logDoc => ({
                _id: logDoc.id,
                ...logDoc.data()
            }));
            console.log(`    ↳ Found ${logsSnapshot.size} log entries in history`);
            }
        } catch (error) {
            console.log(`    ↳ No logs subcollection in history document`);
        }
        }

        operations.push({ insertOne: { document: docData } });
        docCount++;
    }

    if (operations.length > 0) {
        await mongoCollection.bulkWrite(operations, { ordered: false });
        console.log(`  ✅ Migrated ${operations.length} motor_status documents`);
    }
    
    return docCount;
  },


  // 3. watering_schedules: Embedded subcollections
  async 'watering_schedules'() {
    console.log('📊 Migrating watering_schedules...');
    const mongoCollection = client.db('projectisrael_db').collection('watering_schedules');
    const schedulesCollection = firestore.collection('watering_schedules');
    
    const scheduleRoots = await schedulesCollection.listDocuments();
    const operations = [];
    
    for (const rootRef of scheduleRoots) {
      const rootId = rootRef.id;
      const rootData = { _id: rootId };
      
      // Migrate each subcollection type
      const subCollections = ['daily', 'history', 'one_time', 'weekly'];
      
      for (const subCol of subCollections) {
        const subCollectionRef = rootRef.collection(subCol);
        const subSnapshot = await subCollectionRef.get();
        
        if (!subSnapshot.empty) {
          rootData[subCol] = subSnapshot.docs.map(doc => ({
            _id: doc.id,
            ...doc.data()
          }));
          console.log(`  -> ${rootId}/${subCol}: ${subSnapshot.size} entries`);
        }
      }
      
      operations.push({ insertOne: { document: rootData } });
    }
    
    if (operations.length > 0) {
      await mongoCollection.bulkWrite(operations, { ordered: false });
    }
    return operations.length;
  },

  // 4. Simple collections (no subcollections)
  async simpleCollection(collectionName) {
    console.log(`📊 Migrating ${collectionName}...`);
    const mongoCollection = client.db('projectisrael_db').collection(collectionName);
    const firestoreCollection = firestore.collection(collectionName);
    
    const snapshot = await firestoreCollection.get();
    const operations = [];
    
    if (!snapshot.empty) {
      snapshot.docs.forEach(doc => {
        operations.push({
          insertOne: {
            document: {
              _id: doc.id,
              ...doc.data()
            }
          }
        });
      });
      
      await mongoCollection.bulkWrite(operations, { ordered: false });
      console.log(`  -> ${snapshot.size} documents migrated`);
    }
    
    return snapshot.size;
  }
};

// Main migration function
async function migrateAllCollections() {
  try {
    await client.connect();
    console.log('✅ Connected to MongoDB');
    
    const migrationResults = {};
    
    // Define migration order and strategies
    const migrationPlan = [
      { name: 'sensor_readings', handler: collectionHandlers['sensor_readings'] },
      { name: 'app_metrics', handler: () => collectionHandlers.simpleCollection('app_metrics') },
      { name: 'configurations', handler: () => collectionHandlers.simpleCollection('configurations') },
      { name: 'crop_recommendations', handler: () => collectionHandlers.simpleCollection('crop_recommendations') },
      { name: 'metric_history', handler: () => collectionHandlers.simpleCollection('metric_history') },
      { name: 'motor_status', handler: collectionHandlers['motor_status'] },
      { name: 'network', handler: () => collectionHandlers.simpleCollection('network') },
      { name: 'notifications', handler: () => collectionHandlers.simpleCollection('notifications') },
      { name: 'password_reset_codes', handler: () => collectionHandlers.simpleCollection('password_reset_codes') },
      { name: 'system_stats', handler: () => collectionHandlers.simpleCollection('system_stats') },
      { name: 'users', handler: () => collectionHandlers.simpleCollection('users') },
      { name: 'water_level_readings', handler: () => collectionHandlers.simpleCollection('water_level_readings') },
      { name: 'watering_schedules', handler: collectionHandlers['watering_schedules'] }
    ];

    for (const collection of migrationPlan) {
      try {
        console.log(`\n${'='.repeat(50)}`);
        migrationResults[collection.name] = await collection.handler();
        console.log(`✅ ${collection.name}: ${migrationResults[collection.name]} documents`);
        await new Promise(resolve => setTimeout(resolve, 500)); // Throttle
      } catch (error) {
        console.error(`❌ Failed to migrate ${collection.name}:`, error.message);
        migrationResults[collection.name] = { error: error.message };
      }
    }

    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('🎉 MIGRATION COMPLETE - SUMMARY');
    console.log('='.repeat(60));
    
    let totalDocuments = 0;
    for (const [name, count] of Object.entries(migrationResults)) {
      if (typeof count === 'number') {
        console.log(`✅ ${name}: ${count} documents`);
        totalDocuments += count;
      } else {
        console.log(`❌ ${name}: ERROR - ${count.error}`);
      }
    }
    
    console.log('='.repeat(60));
    console.log(`📈 Total Documents Migrated: ${totalDocuments}`);
    console.log('='.foreach (60));

  } catch (error) {
    console.error('💥 Fatal error:', error);
  } finally {
    await client.close();
    console.log('🔌 MongoDB connection closed.');
  }
}

// Run the migration
migrateAllCollections().catch(console.error);