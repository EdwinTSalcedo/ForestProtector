// Helper function to calculate time ranges
function getTimeRange(hoursAgo) {
  const now = new Date();
  const pastTime = new Date(now.getTime() - (hoursAgo * 60 * 60 * 1000));
  return pastTime;
}

module.exports = getTimeRange;