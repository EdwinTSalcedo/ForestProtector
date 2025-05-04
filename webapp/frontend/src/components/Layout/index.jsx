import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

// Drawer icons
import Filter1Icon from '@mui/icons-material/Filter1';
import Filter2Icon from '@mui/icons-material/Filter2';
import Filter3Icon from '@mui/icons-material/Filter3';
import Filter4Icon from '@mui/icons-material/Filter4';
import Filter5Icon from '@mui/icons-material/Filter5';
import Filter6Icon from '@mui/icons-material/Filter6';
import Filter7Icon from '@mui/icons-material/Filter7';
import Filter8Icon from '@mui/icons-material/Filter8';
import Filter9Icon from '@mui/icons-material/Filter9';
import Filter9PlusIcon from '@mui/icons-material/Filter9Plus';

import { AppBar } from './components/AppBar';
import { Drawer } from './components/Drawer';
import { DrawerHeader } from './components/DrawerHeader';

const icons = [
  <Filter1Icon />,
  <Filter2Icon />,
  <Filter3Icon />,
  <Filter4Icon />,
  <Filter5Icon />,
  <Filter6Icon />,
  <Filter7Icon />,
  <Filter8Icon />,
  <Filter9Icon />,
  <Filter9PlusIcon />,
]

export function Layout({ title, numberOfNodes, node, changeNode, children }) {
  const nodes = Array(numberOfNodes).fill(0);

  const theme = useTheme();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open} style={{ backgroundColor: '#56876D' }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={[
              {
                marginRight: 5,
              },
              open && { display: 'none' },
            ]}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            { title }
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" open={open}>
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          {nodes.map((_, index) => (
            <ListItem key={index} disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => changeNode(index + 1)}
                sx={[ 
                  { minHeight: 48, px: 2.5 },
                  open ? { justifyContent: 'initial'} : { justifyContent: 'center'},
                  node === index + 1 ? { backgroundColor: '#d3d3d3' } : {}, // Highlight selected node
                ]}
              >
                <ListItemIcon
                  sx={[
                    { minWidth: 0, justifyContent: 'center' },
                    open ? { mr: 3 } : { mr: 'auto' },
                  ]}
                >
                  { index < 9 ? icons[index] : icons[9] }
                </ListItemIcon>
                <ListItemText
                  primary={`Node ${index + 1}`}
                  sx={[
                    open ? { opacity: 1 } : { opacity: 0 },
                  ]}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <DrawerHeader />
        { children }
      </Box>
    </Box>
  );
}